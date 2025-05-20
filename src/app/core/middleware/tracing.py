from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time
import uuid

class RequestTracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Add trace ID to request state
        request.state.trace_id = request_id
        
        # Log request
        logger.info(
            f"Request {request_id}: {request.method} {request.url} "
            f"Client: {request.client.host}"
        )
        
        try:
            response = await call_next(request)
            
            # Add trace headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(time.time() - start_time)
            
            # Log response
            logger.info(
                f"Response {request_id}: {response.status_code} "
                f"Time: {time.time() - start_time:.3f}s"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error in request {request_id}: {str(e)}")
            raise