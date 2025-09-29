"""Base entity class for domain entities."""

from abc import ABC
from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4


class BaseEntity(ABC):
    """Base class for all domain entities."""
    
    def __init__(self, id: UUID = None) -> None:
        self._id = id or uuid4()
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self._updated_at = datetime.utcnow()
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary representation."""
        return {
            "id": str(self._id),
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }