from beanie import Document
from pydantic import BaseModel, ConfigDict, EmailStr
from fastapi.security import HTTPBasicCredentials

class Admin(Document):
    fullname: str
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
                "password": "3xt3m#",
            }
        }
    )

    class Settings:
        name = "admin"


class AdminSignIn(HTTPBasicCredentials):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"username": "abdul@youngest.dev", "password": "3xt3m#"}
        }
    )


class AdminData(BaseModel):
    fullname: str
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
            }
        }
    )
