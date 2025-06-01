from pydantic import BaseModel, EmailStr, Field


class UserRegistration(BaseModel):
    username: str = Field(
        ..., min_length=2, max_length=20, description="Имя пользователя"
    )
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )


class UserReturn(BaseModel):
    username: str = Field(
        ..., min_length=2, max_length=20, description="Имя пользователя"
    )
    email: EmailStr = Field(..., description="Электронная почта")
    id: int
