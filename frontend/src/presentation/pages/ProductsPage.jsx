import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useProducts } from '../hooks/useProducts';
import { ProductGrid } from '../components/products/ProductGrid';
import { ProductFilters } from '../components/products/ProductFilters';
import { useCartStore } from '../store/cartStore';
import { useUserStore } from '../store/userStore';
import { useCart } from '../hooks/useCart';

export const ProductsPage = () => {
  const { data: products, isLoading } = useProducts();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const { addItem } = useCartStore();
  const { isAuthenticated, user } = useUserStore();
  const navigate = useNavigate();
  
  // Cargar el carrito si el usuario está autenticado
  useCart();

  const categories = useMemo(() => {
    if (!products) return [];
    return [...new Set(products.map((p) => p.category).filter(Boolean))];
  }, [products]);

  const filteredProducts = useMemo(() => {
    if (!products) return [];
    return products.filter((product) => {
      const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.description?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = !selectedCategory || product.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }, [products, searchTerm, selectedCategory]);

  const handleAddToCart = (product) => {
    if (!isAuthenticated) {
      alert('Por favor, inicia sesión para agregar productos al carrito');
      navigate('/login');
      return;
    }
    
    addItem({
      id: `temp-${Date.now()}`,
      product_id: product.id,
      quantity: 1,
      unit_price: product.price,
      subtotal: product.price,
    });

    // Show notification
    alert(`${product.name} agregado al carrito`);
  };

  const handleViewDetails = (product) => {
    navigate(`/products/${product.id}`);
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Nuestros Productos</h1>
        <p className="text-gray-600">Encuentra todo lo que necesitas en un solo lugar</p>
      </div>

      <ProductFilters
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
        categories={categories}
      />

      <div className="mb-4 text-sm text-gray-600">
        Mostrando {filteredProducts.length} de {products?.length || 0} productos
      </div>

      <ProductGrid
        products={filteredProducts}
        isLoading={isLoading}
        onAddToCart={handleAddToCart}
        onViewDetails={handleViewDetails}
      />
    </div>
  );
};
