# src/app/core/exceptions.py

from typing import Optional, Dict, Any
from fastapi import HTTPException

class AutoDevCommanderError(Exception):
    """Base exception for AutoDev Commander"""
    def __init__(
        self, 
        message: str, 
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500
    ):
        self.message = message
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=self.status_code,
            detail={
                "message": self.message,
                "details": self.details,
                "error_type": self.__class__.__name__
            }
        )

# AI Service Exceptions
class AIServiceError(AutoDevCommanderError):
    """Base exception for AI/LLM service errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=500)

class OllamaServiceError(AIServiceError):
    """Errors from Ollama service"""
    pass

class ModelNotLoadedError(OllamaServiceError):
    """Model not loaded or available"""
    def __init__(self, model_name: str):
        super().__init__(
            f"Model {model_name} not loaded",
            {"model": model_name},
            status_code=503
        )

class EmbeddingError(OllamaServiceError):
    """Error generating embeddings"""
    pass

class GenerationError(OllamaServiceError):
    """Error generating text"""
    pass

# Vector Service Exceptions
class VectorServiceError(AutoDevCommanderError):
    """Base exception for vector operations"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=500)

class QdrantServiceError(VectorServiceError):
    """Errors from Qdrant service"""
    pass

class CollectionError(QdrantServiceError):
    """Collection-related errors"""
    pass

class CollectionNotFoundError(CollectionError):
    """Collection does not exist"""
    def __init__(self, collection_name: str):
        super().__init__(
            f"Collection {collection_name} not found",
            {"collection": collection_name},
            status_code=404
        )

class CollectionCreateError(CollectionError):
    """Error creating collection"""
    pass

class VectorOperationError(QdrantServiceError):
    """Vector operation errors"""
    pass

# Workflow Service Exceptions
class WorkflowServiceError(AutoDevCommanderError):
    """Base exception for workflow operations"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=500)

class N8NServiceError(WorkflowServiceError):
    """Errors from n8n service"""
    pass

class WorkflowNotFoundError(N8NServiceError):
    """Workflow not found"""
    def __init__(self, workflow_id: str):
        super().__init__(
            f"Workflow {workflow_id} not found",
            {"workflow_id": workflow_id},
            status_code=404
        )

class WorkflowExecutionError(N8NServiceError):
    """Workflow execution failed"""
    pass

class WorkflowTimeoutError(N8NServiceError):
    """Workflow execution timed out"""
    def __init__(self, execution_id: str):
        super().__init__(
            f"Workflow execution {execution_id} timed out",
            {"execution_id": execution_id},
            status_code=504
        )

# Configuration Exceptions
class ConfigurationError(AutoDevCommanderError):
    """Configuration-related errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=500)

class EnvironmentError(ConfigurationError):
    """Environment variable errors"""
    pass

class ValidationError(AutoDevCommanderError):
    """Validation errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=400)

# Service Connection Exceptions
class ServiceConnectionError(AutoDevCommanderError):
    """Service connection errors"""
    def __init__(self, service: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"{service} service connection error: {message}",
            details,
            status_code=503
        )

# Exception Registry for error handling
EXCEPTION_STATUS_CODES = {
    ModelNotLoadedError: 503,
    CollectionNotFoundError: 404,
    WorkflowNotFoundError: 404,
    WorkflowTimeoutError: 504,
    ValidationError: 400,
    ServiceConnectionError: 503,
    ConfigurationError: 500,
}

def get_status_code(error: Exception) -> int:
    """Get HTTP status code for exception"""
    if isinstance(error, AutoDevCommanderError):
        return error.status_code
    return EXCEPTION_STATUS_CODES.get(type(error), 500)