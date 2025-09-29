"""User domain entity."""

from typing import Optional, Dict, Any
from uuid import UUID

from .base import BaseEntity


class User(BaseEntity):
    """User entity for the user microservice."""

    def __init__(
        self,
        name: str,
        email: str,
        hash_password: str,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        id_user: Optional[UUID] = None,
    ) -> None:
        super().__init__(id_user)
        self.name = name
        self.email = email
        self.hash_password = hash_password
        self.phone = phone
        self.address = address
        self._validate()

    def _validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Name is required")
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
        if not self.hash_password or len(self.hash_password) < 8:
            raise ValueError("Hash password must be at least 8 characters")

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "id_user": self.id,
                "name": self.name,
                "email": self.email,
                "phone": self.phone,
                "address": self.address,
            }
        )
        return base

