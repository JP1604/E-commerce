"""Simplified integration tests for User Service - no database required."""

import pytest
import pytest_asyncio
from uuid import uuid4
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from user_service.domain.entities.user import User


@pytest.mark.asyncio
class TestUserServiceSimple:
    """Simplified integration tests for User Service."""

    async def test_create_user_entity(self):
        """Test creating a user entity."""
        user = User(
            name="Test User",
            email="test@example.com",
            hash_password="hashedpassword123"
        )
        
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.hash_password == "hashedpassword123"
        assert user.id is not None

    async def test_create_user_with_optional_fields(self):
        """Test creating a user with optional fields."""
        user = User(
            name="Complete User",
            email="complete@example.com",
            hash_password="hashedpassword123",
            phone="+1234567890",
            address="123 Main St, City, Country"
        )
        
        assert user.name == "Complete User"
        assert user.email == "complete@example.com"
        assert user.phone == "+1234567890"
        assert user.address == "123 Main St, City, Country"

    async def test_user_validation(self):
        """Test user validation."""
        # Test valid user
        user = User(
            name="Valid User",
            email="valid@example.com",
            hash_password="validpassword123"
        )
        assert user.name == "Valid User"
        
        # Test invalid name
        with pytest.raises(ValueError, match="Name is required"):
            User(
                name="",
                email="test@example.com",
                hash_password="password123"
            )
        
        # Test invalid email
        with pytest.raises(ValueError, match="Valid email is required"):
            User(
                name="Test User",
                email="invalid-email",
                hash_password="password123"
            )
        
        # Test short password
        with pytest.raises(ValueError, match="Hash password must be at least 8 characters"):
            User(
                name="Test User",
                email="test@example.com",
                hash_password="short"
            )

    async def test_user_to_dict(self):
        """Test user serialization."""
        user = User(
            name="Serialization Test User",
            email="serialization@example.com",
            hash_password="hashedpassword123",
            phone="+1234567890",
            address="Test Address"
        )
        
        user_dict = user.to_dict()
        
        assert user_dict["name"] == "Serialization Test User"
        assert user_dict["email"] == "serialization@example.com"
        assert user_dict["phone"] == "+1234567890"
        assert user_dict["address"] == "Test Address"
        assert "id_user" in user_dict
        assert "created_at" in user_dict
        assert "updated_at" in user_dict
        # Note: hash_password is not included in to_dict for security

    async def test_user_email_validation(self):
        """Test user email validation."""
        # Valid emails
        valid_emails = [
            "user@example.com",
            "test.user@domain.co.uk",
            "user+tag@example.org",
            "user123@test-domain.com"
        ]
        
        for email in valid_emails:
            user = User(
                name="Test User",
                email=email,
                hash_password="password123"
            )
            assert user.email == email
        
        # Test one invalid email case
        with pytest.raises(ValueError):
            User(
                name="Test User",
                email="invalid-email",
                hash_password="password123"
            )

    async def test_user_password_validation(self):
        """Test user password validation."""
        # Valid passwords (8+ characters)
        valid_passwords = [
            "password123",
            "verylongpassword",
            "12345678",
            "special@chars#123"
        ]
        
        for password in valid_passwords:
            user = User(
                name="Test User",
                email="test@example.com",
                hash_password=password
            )
            assert user.hash_password == password
        
        # Invalid passwords (less than 8 characters)
        invalid_passwords = [
            "short",
            "1234567",
            "",
            "abc"
        ]
        
        for password in invalid_passwords:
            with pytest.raises(ValueError, match="Hash password must be at least 8 characters"):
                User(
                    name="Test User",
                    email="test@example.com",
                    hash_password=password
                )

    async def test_user_entity_immutability(self):
        """Test that user entity properties are properly set."""
        user = User(
            name="Immutability Test User",
            email="immutability@example.com",
            hash_password="password123",
            phone="+1234567890",
            address="Test Address"
        )
        
        # All properties should be set correctly
        assert user.name == "Immutability Test User"
        assert user.email == "immutability@example.com"
        assert user.hash_password == "password123"
        assert user.phone == "+1234567890"
        assert user.address == "Test Address"
        assert user.id is not None
        assert user.created_at is not None
        assert user.updated_at is not None

    async def test_user_without_optional_fields(self):
        """Test user creation without optional fields."""
        user = User(
            name="Minimal User",
            email="minimal@example.com",
            hash_password="password123"
        )
        
        assert user.name == "Minimal User"
        assert user.email == "minimal@example.com"
        assert user.hash_password == "password123"
        assert user.phone is None
        assert user.address is None
