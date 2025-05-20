from fastapi import FastAPI
from .error import ErrorHandlerMiddleware
from .tracing import RequestTracingMiddleware
from .rate_limit import RateLimitMiddleware
from .metrics import MetricsMiddleware

def setup_middleware(app: FastAPI) -> None:
    """Configure all middleware for the application"""
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(RequestTracingMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(ErrorHandlerMiddleware)