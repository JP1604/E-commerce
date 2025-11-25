// Landing Page Component - Jamar Inspired
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useProducts } from '@presentation/hooks/useProducts';
import { useCart } from '@presentation/hooks/useCart';
import { ProductCard } from '@presentation/components/ProductCard/ProductCard';
import { motion } from 'framer-motion';
import { FaSearch, FaFilter } from 'react-icons/fa';
import './LandingPage.css';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  
  const userId = localStorage.getItem('userId') || '113a034d-7133-40b6-a4e8-a541a9905297';
  
  const { data: products, isLoading, error } = useProducts({
    search: searchTerm,
    category: selectedCategory || undefined,
  });

  const { cart, addItem } = useCart(userId);

  const handleAddToCart = (productId: string) => {
    const product = products?.find(p => p.id === productId);
    if (!product) return;
    
    if (!cart) {
      console.error('Cart not available');
      return;
    }
    
    addItem({
      cartId: cart.id_cart,
      item: {
        product_id: productId,
        quantity: 1,
        price: product.price,
      },
    });
  };

  const categories = products
    ? Array.from(new Set(products.map(p => p.category).filter(Boolean)))
    : [];

  // Categorías destacadas con imágenes
  const featuredCategories = [
    {
      name: 'Muebles',
      description: 'Muebles modernos y funcionales para tu hogar',
      image: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800',
      link: '/category/muebles'
    },
    {
      name: 'Decoración',
      description: 'Decora tu espacio con estilo único',
      image: 'https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800',
      link: '/category/decoracion'
    },
    {
      name: 'Iluminación',
      description: 'Ilumina cada rincón de tu hogar',
      image: 'https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=800',
      link: '/category/iluminacion'
    }
  ];

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Encuentra todo lo que necesitas
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Los mejores productos para tu hogar al mejor precio
          </motion.p>
          
          <motion.div
            className="hero-search"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <input
              type="text"
              placeholder="Buscar productos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <FaSearch className="search-icon" />
          </motion.div>
        </div>
      </section>

      {/* Categories Showcase */}
      <section className="category-showcase">
        <div className="container">
          <div className="category-grid">
            {featuredCategories.map((category, index) => (
              <motion.div
                key={category.name}
                className="category-card"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                onClick={() => navigate(category.link)}
              >
                <img 
                  src={category.image} 
                  alt={category.name} 
                  className="category-image"
                />
                <div className="category-overlay">
                  <h3>{category.name}</h3>
                  <p>{category.description}</p>
                  <span className="category-btn">Ver categoría</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Filters Section */}
      <section className="filters-section">
        <div className="container">
          <div className="filters">
            <FaFilter />
            <button
              className={`filter-btn ${!selectedCategory ? 'active' : ''}`}
              onClick={() => setSelectedCategory(null)}
            >
              Todos
            </button>
            {categories.map((category) => (
              <button
                key={category}
                className={`filter-btn ${selectedCategory === category ? 'active' : ''}`}
                onClick={() => setSelectedCategory(category || null)}
              >
                {category}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="products-section">
        <div className="container">
          <div className="section-header">
            <h2>Productos Destacados</h2>
            <a href="/products" className="view-all-btn">Ver todos</a>
          </div>

          {isLoading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Cargando productos...</p>
            </div>
          )}

          {error && (
            <div className="error">
              <p>⚠️ Error al cargar productos</p>
              <p>{error.message}</p>
            </div>
          )}

          {products && products.length === 0 && (
            <div className="empty-state">
              <p>📦 No se encontraron productos</p>
            </div>
          )}

          {products && products.length > 0 && (
            <div className="products-grid">
              {products.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onAddToCart={handleAddToCart}
                />
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};
