from pydantic import BaseModel, EmailStr, ConfigDict

class SUserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr
    password: str