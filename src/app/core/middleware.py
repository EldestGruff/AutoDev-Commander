# src/app/core/middleware.py
from typing import Callable, Dict, Any
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time
import traceback

from .exceptions import (
    AutoDevCommanderError,
    ServiceConnectionError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    WorkflowError
)

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
        try:
            # Start timer for request
            start_time = time.time()
            
            # Process request
            response = await call_next(request)
            
            # Add processing time header
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            
            return response

        except AutoDevCommanderError as e:
            logger.error(f"AutoDevCommander error: {str(e)}")
            return self._handle_autodev_error(e)
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            return self._handle_unexpected_error(e)

    def _handle_autodev_error(self, error: AutoDevCommanderError) -> JSONResponse:
        error_mapping = {
            ServiceConnectionError: 503,
            ValidationError: 400,
            AuthenticationError: 401,
            AuthorizationError: 403,
            ResourceNotFoundError: 404,
            WorkflowError: 500
        }

        status_code = error_mapping.get(type(error), 500)
        
        error_response = {
            "error": {
                "type": error.__class__.__name__,
                "message": str(error),
                "details": error.details if hasattr(error, 'details') else None
            }
        }

        if self.debug:
            error_response["error"]["traceback"] = traceback.format_exc()

        return JSONResponse(
            status_code=status_code,
            content=error_response
        )

    def _handle_unexpected_error(self, error: Exception) -> JSONResponse:
        error_response = {
            "error": {
                "type": "UnexpectedError",
                "message": "An unexpected error occurred"
            }
        }

        if self.debug:
            error_response.update({
                "error": {
                    "type": error.__class__.__name__,
                    "message": str(error),
                    "traceback": traceback.format_exc()
                }
            })

        return JSONResponse(
            status_code=500,
            content=error_response
        )

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        # Process request and capture timing
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} "
            f"[{process_time:.2f}s] "
            f"{request.method} {request.url}"
        )
        
        return response

def setup_middleware(app: FastAPI) -> None:
    """Setup all middleware for the application"""
    app.add_middleware(
        ErrorHandlerMiddleware,
        debug=app.debug
    )
    app.add_middleware(RequestLoggingMiddleware)