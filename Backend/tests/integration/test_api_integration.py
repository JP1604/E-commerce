"""Integration tests for APIs using HTTP requests."""

import pytest
import httpx
from uuid import uuid4


@pytest.mark.asyncio
class TestAPIIntegration:
    """Integration tests for APIs using HTTP requests."""
    
    @pytest.fixture
    async def client(self):
        """Create HTTP client for testing."""
        async with httpx.AsyncClient() as client:
            yield client
    
    async def test_cart_service_health(self, client):
        """Test cart service health endpoint."""
        # Act
        response = await client.get("http://localhost:8003/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    async def test_create_product_via_api(self, client):
        """Test creating a product via API."""
        # Arrange
        product_data = {
            "name": "Test Product API",
            "description": "A test product created via API",
            "price": 29.99,
            "status": "activo"
        }
        
        # Act
        response = await client.post(
            "http://localhost:8003/api/v1/products/",
            json=product_data
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Product API"
        assert data["price"] == 29.99
        assert data["status"] == "activo"
        assert "id" in data
    
    async def test_create_cart_via_api(self, client):
        """Test creating a cart via API."""
        # Arrange
        user_id = str(uuid4())
        cart_data = {
            "user_id": user_id,
            "status": "activo"
        }
        
        # Act
        response = await client.post(
            "http://localhost:8003/api/v1/carts/",
            json=cart_data
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == user_id
        assert data["status"] == "activo"
        assert "id" in data
    
    async def test_get_products_via_api(self, client):
        """Test getting products via API."""
        # Act
        response = await client.get("http://localhost:8003/api/v1/products/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_user_service_health(self, client):
        """Test user service health endpoint."""
        # Act
        response = await client.get("http://localhost:8001/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    async def test_create_user_via_api(self, client):
        """Test creating a user via API."""
        # Arrange
        user_data = {
            "name": "Test User API",
            "email": "testapi@example.com",
            "hash_password": "hashedpassword123"
        }
        
        # Act
        response = await client.post(
            "http://localhost:8001/api/v1/users/",
            json=user_data
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test User API"
        assert data["email"] == "testapi@example.com"
        assert "id" in data
    
    async def test_api_gateway_health(self, client):
        """Test API Gateway health endpoint."""
        # Act
        response = await client.get("http://localhost:8080/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    async def test_api_gateway_routes(self, client):
        """Test API Gateway routes."""
        # Test different service routes through API Gateway
        routes_to_test = [
            "/api/v1/products/",
            "/api/v1/users/",
            "/api/v1/carts/",
            "/api/v1/orders/",
            "/api/v1/payments/",
            "/api/v1/deliveries/"
        ]
        
        for route in routes_to_test:
            # Act
            response = await client.get(f"http://localhost:8080{route}")
            
            # Assert - Should not return 404 (route exists)
            assert response.status_code != 404, f"Route {route} not found"
