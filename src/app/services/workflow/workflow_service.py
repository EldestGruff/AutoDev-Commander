async def monitor_execution(self, execution_id: str) -> None:
    """Monitor workflow execution in background"""
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        status = await self.get_execution_status(execution_id)
        if status["status"] in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]:
            break
            
        await asyncio.sleep(2)
        attempt += 1

async def list_workflows(self) -> List[Dict[str, Any]]:
    """List all workflows"""
    return await self.n8n.list_workflows()

async def delete_workflow(self, workflow_id: str) -> None:
    """Delete a workflow"""
    await self.n8n.delete_workflow(workflow_id)

async def pause_workflow(self, workflow_id: str) -> None:
    """Pause a workflow"""
    await self.n8n.update_workflow_state(workflow_id, active=False)

async def resume_workflow(self, workflow_id: str) -> None:
    """Resume a workflow"""
    await self.n8n.update_workflow_state(workflow_id, active=True)

async def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
    """Get detailed execution status"""
    status = await self.n8n.get_workflow_status(execution_id)
    return {
        "status": status,
        "details": await self.n8n.get_execution_details(execution_id)
    }
