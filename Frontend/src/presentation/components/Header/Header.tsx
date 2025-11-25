// Header Component - Jamar Inspired
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaShoppingCart, FaUser, FaUserPlus, FaSearch, FaMapMarkerAlt } from 'react-icons/fa';
import { useCart } from '@presentation/hooks/useCart';
import './Header.css';

export const Header: React.FC = () => {
  const userId = localStorage.getItem('userId') || '113a034d-7133-40b6-a4e8-a541a9905297';
  const { cart } = useCart(userId);
  const [searchQuery, setSearchQuery] = useState('');

  const cartItemsCount = cart?.items?.reduce((sum: number, item: any) => sum + item.quantity, 0) || 0;

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implementar búsqueda
    console.log('Buscar:', searchQuery);
  };

  return (
    <header className="header">
      <div className="header-container">
        {/* Logo */}
        <Link to="/" className="logo">
          <span className="logo-icon">🛍️</span>
          <span className="logo-text">Mi Tienda</span>
        </Link>

        {/* Search Bar */}
        <div className="search-container">
          <form onSubmit={handleSearch} className="search-wrapper">
            <input
              type="text"
              className="search-input"
              placeholder="Encuentra algo extraordinario..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="search-icon" style={{ background: 'none', border: 'none' }}>
              <FaSearch />
            </button>
          </form>
        </div>

        {/* Navigation */}
        <nav className="nav">
          <Link to="/" className="nav-link">Inicio</Link>
          <Link to="/products" className="nav-link">Productos</Link>
          <Link to="/categories" className="nav-link">Categorías</Link>
          <Link to="/offers" className="nav-link">Ofertas</Link>
        </nav>

        {/* Actions */}
        <div className="header-actions">
          <Link to="/register" className="register-btn">
            <FaUserPlus />
            <span>Registrarse</span>
          </Link>

          <Link to="/profile" className="icon-btn" title="Mi cuenta">
            <FaUser />
          </Link>

          <Link to="/cart" className="icon-btn cart-btn" title="Carrito">
            <FaShoppingCart />
            {cartItemsCount > 0 && (
              <span className="cart-badge">{cartItemsCount}</span>
            )}
          </Link>
        </div>
      </div>
    </header>
  );
};
