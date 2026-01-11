from pydantic import BaseModel


class ServerConfig(BaseModel):
    SERVER_NAME: str = "Booking Management System API"
    SERVER_DESCRIPTION: str = "Resource booking service"

    API_VERSION: str = "0.0.1"

    DEBUG: bool = False
    SWAGGER_ENABLE: bool = True
    EXCEPT_LOG: bool = False

    swagger_ui_parameters: dict = {
        "docExpansion": "none",
        "filter": True,
        "displayRequestDuration": True,
        "deepLinking": True,
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": 1,
        "operationsSorter": "method",
    }

    server_responces: dict = {
        400: {"description": "Bad Reques"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
        422: {"description": "Validation Error"},
    }
