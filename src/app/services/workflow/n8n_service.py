from typing import Dict, Any, Optional, List
import httpx
from loguru import logger
from ...core.config import settings
from ...schemas.workflow import WorkflowStatus, WorkflowCreate

class N8NService:
    def __init__(self):
        self.base_url = f"{settings.N8N_PROTOCOL}://{settings.N8N_HOST}:{settings.N8N_PORT}"
        self.api_url = f"{self.base_url}/api/v1"
        self._session: Optional[httpx.AsyncClient] = None

    async def get_session(self) -> httpx.AsyncClient:
        if self._session is None:
            self._session = httpx.AsyncClient(base_url=self.api_url)
        return self._session

    async def create_workflow(self, workflow: WorkflowCreate) -> Dict[str, Any]:
        """Create a new n8n workflow."""
        session = await self.get_session()
        try:
            response = await session.post(
                "/workflows",
                json={
                    "name": workflow.name,
                    "nodes": workflow.nodes,
                    "connections": {},
                    "active": True,
                    "settings": {
                        "saveManualExecutions": True,
                        "saveExecutionProgress": True,
                    }
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating workflow: {e}")
            raise

    async def trigger_workflow(
        self,
        workflow_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Trigger an n8n workflow."""
        session = await self.get_session()
        try:
            response = await session.post(
                f"/workflows/{workflow_id}/execute",
                json={"data": data}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error triggering workflow: {e}")
            raise

    async def get_workflow_status(self, execution_id: str) -> WorkflowStatus:
        """Get workflow execution status."""
        session = await self.get_session()
        try:
            response = await session.get(f"/executions/{execution_id}")
            response.raise_for_status()
            data = response.json()
            
            if data["finished"]:
                return WorkflowStatus.COMPLETED if data["success"] else WorkflowStatus.FAILED
            return WorkflowStatus.RUNNING
        except Exception as e:
            logger.error(f"Error getting workflow status: {e}")
            raise

    async def close(self):
        """Close the HTTP session."""
        if self._session:
            await self._session.aclose()
            self._session = None
