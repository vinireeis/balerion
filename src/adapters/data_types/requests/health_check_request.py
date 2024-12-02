from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    api_status: str
    service: str
    version: str
