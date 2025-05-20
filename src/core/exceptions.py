# src/app/core/exceptions.py
from typing import Optional

class AutoDevCommanderError(Exception):
    """Base exception for AutoDev Commander"""
    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class WorkflowError(AutoDevCommanderError):
    """Base exception for workflow-related errors"""
    pass

class WorkflowNotFoundError(WorkflowError):
    """Raised when a workflow is not found"""
    pass

class WorkflowExecutionError(WorkflowError):
    """Raised when workflow execution fails"""
    pass

class WorkflowValidationError(WorkflowError):
    """Raised when workflow validation fails"""
    pass

class ServiceConnectionError(AutoDevCommanderError):
    """Raised when service connection fails"""
    pass

class ServiceTimeoutError(AutoDevCommanderError):
    """Raised when service operation times out"""
    pass

class ConfigurationError(AutoDevCommanderError):
    """Raised when configuration is invalid"""
    pass

class ResourceNotFoundError(AutoDevCommanderError):
    """Raised when a resource is not found"""
    pass

class AuthenticationError(AutoDevCommanderError):
    """Raised when authentication fails"""
    pass

class AuthorizationError(AutoDevCommanderError):
    """Raised when authorization fails"""
    pass

class ValidationError(AutoDevCommanderError):
    """Raised when validation fails"""
    pass

class RateLimitError(AutoDevCommanderError):
    """Raised when rate limit is exceeded"""
    pass

# AI Service Exceptions
class AIServiceError(AutoDevCommanderError):
    """Base exception for AI service errors"""
    pass

class ModelNotFoundError(AIServiceError):
    """Raised when AI model is not found"""
    pass

class InvalidPromptError(AIServiceError):
    """Raised when prompt is invalid"""
    pass

# Vector Service Exceptions
class VectorServiceError(AutoDevCommanderError):
    """Base exception for vector service errors"""
    pass

class CollectionNotFoundError(VectorServiceError):
    """Raised when collection is not found"""
    pass

class VectorDimensionError(VectorServiceError):
    """Raised when vector dimensions don't match"""
    pass

# Workflow Service Exceptions
class WorkflowTemplateError(WorkflowError):
    """Raised when template operation fails"""
    pass

class WorkflowStateError(WorkflowError):
    """Raised when workflow state transition is invalid"""
    pass

# Error Mapping for HTTP Responses
HTTP_ERROR_MAPPING = {
    WorkflowNotFoundError: 404,
    WorkflowValidationError: 400,
    WorkflowExecutionError: 500,
    ServiceConnectionError: 503,
    ServiceTimeoutError: 504,
    ConfigurationError: 500,
    ResourceNotFoundError: 404,
    AuthenticationError: 401,
    AuthorizationError: 403,
    ValidationError: 400,
    RateLimitError: 429,
    ModelNotFoundError: 404,
    InvalidPromptError: 400,
    CollectionNotFoundError: 404,
    VectorDimensionError: 400,
    WorkflowTemplateError: 400,
    WorkflowStateError: 400,
}

def get_error_code(error: Exception) -> int:
    """Get HTTP error code for exception"""
    return HTTP_ERROR_MAPPING.get(type(error), 500)