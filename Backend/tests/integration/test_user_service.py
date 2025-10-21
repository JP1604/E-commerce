"""Integration tests for User Service."""

import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

# Add the user_service to the path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from user_service.domain.entities.user import User
from user_service.infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepository


@pytest.mark.asyncio
class TestUserServiceIntegration:
    """Integration tests for User Service with database."""
    
    async def test_create_user(self, user_db_session: AsyncSession):
        """Test creating a user in the database."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        user = User(
            name="Test User",
            email="test@example.com",
            hash_password="hashedpassword123"
        )
        
        # Act
        created_user = await user_repo.create(user)
        
        # Assert
        assert created_user.id is not None
        assert created_user.email == "test@example.com"
        assert created_user.name == "Test User"
        assert created_user.hash_password == "hashedpassword123"
        assert created_user.created_at is not None
        assert created_user.updated_at is not None
    
    async def test_get_user_by_id(self, user_db_session: AsyncSession):
        """Test retrieving a user by ID."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        user = User(
            email="retrieval@example.com",
            username="retrievaluser",
            full_name="Retrieval User",
            status=UserStatus.ACTIVE
        )
        created_user = await user_repo.create(user)
        
        # Act
        retrieved_user = await user_repo.get_by_id(created_user.id)
        
        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == "retrieval@example.com"
        assert retrieved_user.username == "retrievaluser"
    
    async def test_get_user_by_email(self, user_db_session: AsyncSession):
        """Test retrieving a user by email."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        user = User(
            email="emailtest@example.com",
            username="emailuser",
            full_name="Email Test User",
            status=UserStatus.ACTIVE
        )
        created_user = await user_repo.create(user)
        
        # Act
        retrieved_user = await user_repo.get_by_email("emailtest@example.com")
        
        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == "emailtest@example.com"
    
    async def test_get_user_by_username(self, user_db_session: AsyncSession):
        """Test retrieving a user by username."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        user = User(
            email="usernametest@example.com",
            username="usernametest",
            full_name="Username Test User",
            status=UserStatus.ACTIVE
        )
        created_user = await user_repo.create(user)
        
        # Act
        retrieved_user = await user_repo.get_by_username("usernametest")
        
        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.username == "usernametest"
    
    async def test_get_nonexistent_user(self, user_db_session: AsyncSession):
        """Test retrieving a non-existent user returns None."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        nonexistent_id = uuid4()
        
        # Act
        retrieved_user = await user_repo.get_by_id(nonexistent_id)
        
        # Assert
        assert retrieved_user is None
    
    async def test_list_users(self, user_db_session: AsyncSession):
        """Test listing all users."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        
        # Create multiple users
        users = [
            User(
                email=f"user{i}@example.com",
                username=f"user{i}",
                full_name=f"User {i}",
                status=UserStatus.ACTIVE
            )
            for i in range(3)
        ]
        
        for user in users:
            await user_repo.create(user)
        
        # Act
        all_users = await user_repo.list_all()
        
        # Assert
        assert len(all_users) >= 3
        usernames = [u.username for u in all_users]
        assert "user0" in usernames
        assert "user1" in usernames
        assert "user2" in usernames
    
    async def test_update_user(self, user_db_session: AsyncSession):
        """Test updating a user."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        user = User(
            email="original@example.com",
            username="originaluser",
            full_name="Original User",
            status=UserStatus.ACTIVE
        )
        created_user = await user_repo.create(user)
        
        # Act
        created_user.full_name = "Updated User"
        created_user.email = "updated@example.com"
        updated_user = await user_repo.update(created_user)
        
        # Assert
        assert updated_user.full_name == "Updated User"
        assert updated_user.email == "updated@example.com"
        assert updated_user.updated_at > created_user.created_at
    
    async def test_delete_user(self, user_db_session: AsyncSession):
        """Test deleting a user."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        user = User(
            email="delete@example.com",
            username="deleteuser",
            full_name="User to Delete",
            status=UserStatus.ACTIVE
        )
        created_user = await user_repo.create(user)
        
        # Act
        await user_repo.delete(created_user.id)
        
        # Assert
        deleted_user = await user_repo.get_by_id(created_user.id)
        assert deleted_user is None
    
    async def test_user_status_enum(self, user_db_session: AsyncSession):
        """Test user status enum values."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        
        # Test ACTIVE status
        active_user = User(
            email="active@example.com",
            username="activeuser",
            full_name="Active User",
            status=UserStatus.ACTIVE
        )
        created_active = await user_repo.create(active_user)
        assert created_active.status == UserStatus.ACTIVE
        
        # Test INACTIVE status
        inactive_user = User(
            email="inactive@example.com",
            username="inactiveuser", 
            full_name="Inactive User",
            status=UserStatus.INACTIVE
        )
        created_inactive = await user_repo.create(inactive_user)
        assert created_inactive.status == UserStatus.INACTIVE
    
    async def test_unique_email_constraint(self, user_db_session: AsyncSession):
        """Test that email uniqueness is enforced."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        user1 = User(
            email="unique@example.com",
            username="user1",
            full_name="User 1",
            status=UserStatus.ACTIVE
        )
        user2 = User(
            email="unique@example.com",  # Same email
            username="user2",
            full_name="User 2",
            status=UserStatus.ACTIVE
        )
        
        # Act & Assert
        await user_repo.create(user1)
        
        # This should raise an exception due to unique constraint
        with pytest.raises(Exception):  # Could be IntegrityError or similar
            await user_repo.create(user2)
    
    async def test_unique_username_constraint(self, user_db_session: AsyncSession):
        """Test that username uniqueness is enforced."""
        # Arrange
        user_repo = SQLAlchemyUserRepository(user_db_session)
        user1 = User(
            email="user1@example.com",
            username="uniqueuser",
            full_name="User 1",
            status=UserStatus.ACTIVE
        )
        user2 = User(
            email="user2@example.com",
            username="uniqueuser",  # Same username
            full_name="User 2",
            status=UserStatus.ACTIVE
        )
        
        # Act & Assert
        await user_repo.create(user1)
        
        # This should raise an exception due to unique constraint
        with pytest.raises(Exception):  # Could be IntegrityError or similar
            await user_repo.create(user2)
