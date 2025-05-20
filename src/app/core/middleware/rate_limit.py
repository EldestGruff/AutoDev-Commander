from typing import Callable, Dict, Tuple
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import time
import asyncio
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        rate_limit: int = 100,  # requests per minute
        window: int = 60  # window size in seconds
    ):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.window = window
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        client_ip = request.client.host
        
        async with self.lock:
            now = time.time()
            
            # Clean old requests
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if now - req_time < self.window
            ]
            
            # Check rate limit
            if len(self.requests[client_ip]) >= self.rate_limit:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "retry_after": self.window - (now - self.requests[client_ip][0])
                    }
                )
            
            # Add new request
            self.requests[client_ip].append(now)
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.rate_limit)
        response.headers["X-RateLimit-Remaining"] = str(
            self.rate_limit - len(self.requests[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(self.requests[client_ip][0] + self.window)
        )
        
        return response