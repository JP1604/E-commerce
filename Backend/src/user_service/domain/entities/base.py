"""Base entity with timestamps and UUID id."""

from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Dict, Any


class BaseEntity:
    """Base domain entity with common fields and helpers."""

    def __init__(self, id: Optional[UUID] = None) -> None:
        self.id = id or uuid4()
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    def update_timestamp(self) -> None:
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

