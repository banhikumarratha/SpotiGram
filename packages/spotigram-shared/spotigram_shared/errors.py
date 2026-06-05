class SpotigramError(Exception):
    """Base exception for all Spotigram errors."""
    pass

class ResourceNotFoundError(SpotigramError):
    """Raised when a resource is not found."""
    pass

class IntegrationError(SpotigramError):
    """Raised when an external integration fails."""
    pass

class BusinessLogicError(SpotigramError):
    """Raised when a business rule is violated."""
    pass

def setup_exception_handlers(app):
    from fastapi import Request, FastAPI
    from fastapi.responses import JSONResponse
    import traceback

    @app.exception_handler(ResourceNotFoundError)
    async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "type": "https://spotigram.ai/errors/not-found",
                "title": "Resource Not Found",
                "status": 404,
                "detail": str(exc),
                "instance": str(request.url)
            }
        )

    @app.exception_handler(BusinessLogicError)
    async def business_logic_handler(request: Request, exc: BusinessLogicError):
        return JSONResponse(
            status_code=422,
            content={
                "type": "https://spotigram.ai/errors/business-logic",
                "title": "Unprocessable Entity",
                "status": 422,
                "detail": str(exc),
                "instance": str(request.url)
            }
        )

    @app.exception_handler(IntegrationError)
    async def integration_error_handler(request: Request, exc: IntegrationError):
        return JSONResponse(
            status_code=502,
            content={
                "type": "https://spotigram.ai/errors/integration-failure",
                "title": "Bad Gateway",
                "status": 502,
                "detail": str(exc),
                "instance": str(request.url)
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # We only catch generic exceptions here to format them nicely
        return JSONResponse(
            status_code=500,
            content={
                "type": "https://spotigram.ai/errors/internal-server-error",
                "title": "Internal Server Error",
                "status": 500,
                "detail": "An unexpected error occurred.",
                "instance": str(request.url),
                # "traceback": traceback.format_exc() # Removed for security in prod, but could be added if ENVIRONMENT=dev
            }
        )

