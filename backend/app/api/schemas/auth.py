# from uuid import UUID

# from pydantic import BaseModel


# class LoginResponse(BaseModel):
#     access_token: str
#     token_type: str = "bearer"
#     user_id: UUID


# class RegisterRequest(BaseModel):
#     email: EmailStr
#     password: str


# class RegisterResponse(BaseModel):
#     id: UUID
#     email: EmailStr
#     created_at: datetime
