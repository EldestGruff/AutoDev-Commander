# src/app/core/middleware.py
from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import AutoDevCommanderError, get_error_code
from loguru import logger

async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except AutoDevCommanderError as e:
        status_code = get_error_code(e)
        logger.error(f"AutoDevCommander error: {e.message}")
        return JSONResponse(
            status_code=status_code,
            content={
                "error": e.message,
                "details": e.details,
                "type": e.__class__.__name__
            }
        )
    except Exception as e:
        logger.exception("Unexpected error")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "type": "UnexpectedError",
                "details": {"message": str(e)}
            }
        )