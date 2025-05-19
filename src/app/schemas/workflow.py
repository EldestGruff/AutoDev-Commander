from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import Enum

class WorkflowTriggerType(str, Enum):
    MANUAL = "manual"
    WEBHOOK = "webhook"
    SCHEDULED = "scheduled"

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowCreate(BaseModel):
    name: str = Field(..., description="Name of the workflow")
    description: Optional[str] = Field(None, description="Workflow description")
    trigger_type: WorkflowTriggerType = Field(..., description="Type of trigger")
    nodes: List[Dict[str, Any]] = Field(..., description="Workflow nodes configuration")

class WorkflowTrigger(BaseModel):
    workflow_id: str = Field(..., description="ID of the workflow to trigger")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Input data for workflow")

class WorkflowResponse(BaseModel):
    id: str
    status: WorkflowStatus
    result: Optional[Dict[str, Any]] = None
