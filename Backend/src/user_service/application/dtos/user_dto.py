"""User DTOs."""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None


class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    current_password: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserResponseDTO(BaseModel):
    id_user: UUID
    name: str
    email: EmailStr
    phone: Optional[str]
    address: Optional[str]
    created_at: datetime
    last_updated: datetime

    @classmethod
    def from_entity(cls, user):
        return cls(
            id_user=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            address=user.address,
            created_at=user.created_at,
            last_updated=user.updated_at,
        )


class LoginDTO(BaseModel):
    email: EmailStr
    password: str
