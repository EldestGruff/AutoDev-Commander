from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime
import json
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field
import httpx
from loguru import logger

from ...core.config import settings
from ...core.exceptions import WorkflowError, WorkflowNotFoundError

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowPriority(int, Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class WorkflowDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[Dict[str, Any]]
    connections: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    settings: Dict[str, Any] = Field(default_factory=dict)

class WorkflowExecution(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    workflow_id: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class WorkflowService:
    def __init__(self):
        self.base_url = f"{settings.N8N_PROTOCOL}://{settings.N8N_HOST}:{settings.N8N_PORT}/api/v1"
        self._session: Optional[httpx.AsyncClient] = None
        self.executions: Dict[UUID, WorkflowExecution] = {}

    async def get_session(self) -> httpx.AsyncClient:
        """Get or create HTTP session"""
        if self._session is None:
            self._session = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            )
        return self._session

    async def create_workflow(self, definition: WorkflowDefinition) -> Dict[str, Any]:
        """Create a new workflow in n8n"""
        try:
            session = await self.get_session()
            response = await session.post(
                "/workflows",
                json={
                    "name": definition.name,
                    "nodes": definition.nodes,
                    "connections": definition.connections,
                    "settings": {
                        **definition.settings,
                        "saveManualExecutions": True,
                        "saveExecutionProgress": True
                    },
                    "tags": definition.tags
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to create workflow: {e}")
            raise WorkflowError(f"Failed to create workflow: {str(e)}")

    async def execute_workflow(
        self,
        workflow_id: str,
        input_, Any],
        priority: WorkflowPriority = WorkflowPriority.MEDIUM
    ) -> WorkflowExecution:
        """Execute a workflow with input data"""
        try:
            session = await self.get_session()
            response = await session.post(
                f"/workflows/{workflow_id}/execute",
                json={
                    "data": input_data,
                    "priority": priority.value
                }
            )
            response.raise_for_status()
            data = response.json()

            execution = WorkflowExecution(
                workflow_id=workflow_id,
                status=WorkflowStatus.RUNNING
            )
            self.executions[execution.id] = execution

            # Start monitoring execution
            asyncio.create_task(self._monitor_execution(execution.id, data["executionId"]))

            return execution
        except httpx.HTTPError as e:
            logger.error(f"Failed to execute workflow: {e}")
            raise WorkflowError(f"Failed to execute workflow: {str(e)}")

    async def _monitor_execution(self, execution_id: UUID, n8n_execution_id: str):
        """Monitor workflow execution status"""
        try:
            while True:
                status = await self.get_execution_status(n8n_execution_id)
                execution = self.executions[execution_id]
                
                if status["finished"]:
                    execution.status = (
                        WorkflowStatus.COMPLETED if status["success"]
                        else WorkflowStatus.FAILED
                    )
                    execution.completed_at = datetime.utcnow()
                    execution.result = status.get("data", {})
                    if not status["success"]:
                        execution.error = status.get("error", "Unknown error")
                    break

                await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"Error monitoring execution {execution_id}: {e}")
            if execution_id in self.executions:
                self.executions[execution_id].status = WorkflowStatus.FAILED
                self.executions[execution_id].error = str(e)

    async def get_execution_status(self, n8n_execution_id: str) -> Dict[str, Any]:
        """Get workflow execution status from n8n"""
        try:
            session = await self.get_session()
            response = await session.get(f"/executions/{n8n_execution_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to get execution status: {e}")
            raise WorkflowError(f"Failed to get execution status: {str(e)}")

    async def get_workflow_execution(self, execution_id: UUID) -> WorkflowExecution:
        """Get workflow execution details"""
        if execution_id not in self.executions:
            raise WorkflowNotFoundError(f"Execution {execution_id} not found")
        return self.executions[execution_id]

    async def list_workflows(
        self,
        tags: Optional[List[str]] = None,
        active: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """List workflows with optional filtering"""
        try:
            session = await self.get_session()
            params = {}
            if tags:
                params["tags"] = ",".join(tags)
            if active is not None:
                params["active"] = str(active).lower()

            response = await session.get("/workflows", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to list workflows: {e}")
            raise WorkflowError(f"Failed to list workflows: {str(e)}")

    async def delete_workflow(self, workflow_id: str):
        """Delete a workflow"""
        try:
            session = await self.get_session()
            response = await session.delete(f"/workflows/{workflow_id}")
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"Failed to delete workflow: {e}")
            raise WorkflowError(f"Failed to delete workflow: {str(e)}")

    async def update_workflow(
        self,
        workflow_id: str,
        definition: WorkflowDefinition
    ) -> Dict[str, Any]:
        """Update an existing workflow"""
        try:
            session = await self.get_session()
            response = await session.put(
                f"/workflows/{workflow_id}",
                json={
                    "name": definition.name,
                    "nodes": definition.nodes,
                    "connections": definition.connections,
                    "settings": definition.settings,
                    "tags": definition.tags
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to update workflow: {e}")
            raise WorkflowError(f"Failed to update workflow: {str(e)}")

    async def cleanup(self):
        """Cleanup service resources"""
        if self._session:
            await self._session.aclose()
            self._session = None