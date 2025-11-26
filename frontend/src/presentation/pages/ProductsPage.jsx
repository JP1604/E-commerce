import React, { useState, useMemo } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useProducts } from '../hooks/useProducts';
import { ProductGrid } from '../components/products/ProductGrid';
import { ProductFilters } from '../components/products/ProductFilters';
import { useCartStore } from '../store/cartStore';
import { useUserStore } from '../store/userStore';
import { useCart } from '../hooks/useCart';
import { Button } from '../components/ui/Button';
import { Card, CardBody } from '../components/ui/Card';

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
      {/* Header with Sell Button */}
      <div className="mb-8 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Nuestros Productos</h1>
          <p className="text-gray-600">Encuentra todo lo que necesitas en un solo lugar</p>
        </div>
        
        {/* Sell Products CTA Card */}
        <Card className="lg:max-w-md border-2 border-accent-200 bg-gradient-to-br from-accent-50 to-primary-50">
          <CardBody className="p-6">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-500 to-primary-500 flex items-center justify-center">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </div>
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-gray-900 mb-1">¿Tienes algo para vender?</h3>
                <p className="text-sm text-gray-600 mb-3">
                  Publica tus productos gratis y alcanza miles de clientes
                </p>
                <Link to="/sell-products">
                  <Button size="sm" className="btn-gradient shadow-md hover:shadow-lg w-full">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    Vende tus productos
                  </Button>
                </Link>
              </div>
            </div>
          </CardBody>
        </Card>
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
