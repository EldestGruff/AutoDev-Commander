from typing import Callable, Dict, Any
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time
import traceback
import uuid

from ..exceptions import AutoDevCommanderError

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        debug: bool = False
    ):
        super().__init__(app)
        self.debug = debug

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        error_id = str(uuid.uuid4())
        request.state.error_id = error_id
        
        try:
            response = await call_next(request)
            return response
            
        except AutoDevCommanderError as e:
            logger.error(f"Error ID {error_id}: {str(e)}")
            return self._handle_known_error(e, error_id)
            
        except Exception as e:
            logger.error(f"Error ID {error_id}: Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            return self._handle_unknown_error(e, error_id)

    def _handle_known_error(
        self,
        error: AutoDevCommanderError,
        error_id: str
    ) -> JSONResponse:
        error_response = {
            "error": {
                "id": error_id,
                "type": error.__class__.__name__,
                "message": str(error),
                "details": error.details if hasattr(error, 'details') else None
            }
        }

        if self.debug:
            error_response["error"]["traceback"] = traceback.format_exc()

        return JSONResponse(
            status_code=error.status_code,
            content=error_response
        )

    def _handle_unknown_error(
        self,
        error: Exception,
        error_id: str
    ) -> JSONResponse:
        error_response = {
            "error": {
                "id": error_id,
                "type": "UnexpectedError",
                "message": "An unexpected error occurred"
            }
        }

        if self.debug:
            error_response["error"].update({
                "type": error.__class__.__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            })

        return JSONResponse(
            status_code=500,
            content=error_response
        )