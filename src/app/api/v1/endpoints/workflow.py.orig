from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from ....core.di import get_n8n_service
from ....services.workflow.n8n_service import N8NService
from ....services.workflow.workflow_service import WorkflowService
from ....services.workflow.templates import WorkflowTemplate
from ....schemas.workflow import (
    WorkflowCreate,
    WorkflowTrigger,
    WorkflowResponse,
    WorkflowStatus
)

router = APIRouter()

# Request/Response Models
class TemplateWorkflowRequest(BaseModel):
    template_type: WorkflowTemplate
    customization: Optional[Dict[str, Any]] = None

class WorkflowExecuteRequest(BaseModel):
    workflow_id: str
    input_data: Dict[str, Any]

class WorkflowListResponse(BaseModel):
    workflows: List[Dict[str, Any]]

# Dependency Injection
def get_workflow_service(
    n8n_service: N8NService = Depends(get_n8n_service)
) -> WorkflowService:
    return WorkflowService(n8n_service)

@router.post("/templates", response_model=Dict[str, Any])
async def create_from_template(
    request: TemplateWorkflowRequest,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Create a workflow from a template"""
    try:
        workflow = await workflow_service.create_from_template(
            request.template_type,
            request.customization
        )
        return {
            "status": "success",
            "workflow_id": workflow["id"],
            "message": f"Workflow created from template {request.template_type.value}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create workflow from template: {str(e)}"
        )

@router.post("/execute", response_model=WorkflowResponse)
async def execute_workflow(
    request: WorkflowExecuteRequest,
    background_tasks: BackgroundTasks,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Execute a workflow"""
    try:
        result = await workflow_service.execute_workflow(
            request.workflow_id,
            request.input_data
        )
        
        # Add status check to background tasks
        background_tasks.add_task(
            workflow_service.monitor_execution,
            result["execution_id"]
        )
        
        return WorkflowResponse(
            id=result["execution_id"],
            status=WorkflowStatus.PENDING,
            result={"message": "Workflow execution started"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute workflow: {str(e)}"
        )

@router.get("/status/{execution_id}", response_model=WorkflowResponse)
async def get_execution_status(
    execution_id: str,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Get workflow execution status"""
    try:
        status = await workflow_service.get_execution_status(execution_id)
        return WorkflowResponse(
            id=execution_id,
            status=status["status"],
            result=status["details"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get workflow status: {str(e)}"
        )

@router.get("/list", response_model=WorkflowListResponse)
async def list_workflows(
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """List all workflows"""
    try:
        workflows = await workflow_service.list_workflows()
        return WorkflowListResponse(workflows=workflows)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list workflows: {str(e)}"
        )

@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: str,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Delete a workflow"""
    try:
        await workflow_service.delete_workflow(workflow_id)
        return {"status": "success", "message": f"Workflow {workflow_id} deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete workflow: {str(e)}"
        )

@router.post("/{workflow_id}/pause")
async def pause_workflow(
    workflow_id: str,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Pause a workflow"""
    try:
        await workflow_service.pause_workflow(workflow_id)
        return {"status": "success", "message": f"Workflow {workflow_id} paused"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to pause workflow: {str(e)}"
        )

@router.post("/{workflow_id}/resume")
async def resume_workflow(
    workflow_id: str,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """Resume a workflow"""
    try:
        await workflow_service.resume_workflow(workflow_id)
        return {"status": "success", "message": f"Workflow {workflow_id} resumed"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to resume workflow: {str(e)}"
        )
