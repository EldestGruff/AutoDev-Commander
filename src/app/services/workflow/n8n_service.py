from typing import Dict, Any, Optional
import httpx
from loguru import logger

from ...core.config import settings

class N8NService:
    def __init__(self):
        self.base_url = f"{settings.N8N_PROTOCOL}://{settings.N8N_HOST}:{settings.N8N_PORT}"
        self.api_url = f"{self.base_url}/api/v1"

    async def trigger_workflow(
        self,
        workflow_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Trigger an n8n workflow."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_url}/workflows/{workflow_id}",
                    json=data
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Error triggering workflow: {e}")
                raise

    async def get_workflow_status(
        self,
        execution_id: str
    ) -> Dict[str, Any]:
        """Get workflow execution status."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.api_url}/executions/{execution_id}"
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Error getting workflow status: {e}")
                raise
