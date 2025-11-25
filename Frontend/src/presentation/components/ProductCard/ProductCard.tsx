// Product Card Component
import { Product } from '@domain/entities/Product';
import { motion } from 'framer-motion';
import { FaShoppingCart, FaEye } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import './ProductCard.css';

interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: string) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, onAddToCart }) => {
  const navigate = useNavigate();

  const handleAddToCart = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent card click
    onAddToCart(product.id);
  };

  const handleViewDetails = () => {
    navigate(`/product/${product.id}`);
  };

  return (
    <motion.div
      className="product-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -8, boxShadow: '0 12px 24px rgba(0,0,0,0.1)' }}
      transition={{ duration: 0.3 }}
      onClick={handleViewDetails}
      style={{ cursor: 'pointer' }}
    >
      <div className="product-image">
        {product.image_url ? (
          <img src={product.image_url} alt={product.name} />
        ) : (
          <div className="product-image-placeholder">
            <span>📦</span>
          </div>
        )}
        {product.stock_quantity < 10 && product.stock_quantity > 0 && (
          <span className="stock-badge low-stock">
            ¡Solo {product.stock_quantity} disponibles!
          </span>
        )}
        {product.stock_quantity === 0 && (
          <span className="stock-badge out-of-stock">Agotado</span>
        )}
        
        {/* View Details Overlay */}
        <div className="product-overlay">
          <FaEye />
          <span>Ver detalles</span>
        </div>
      </div>

      <div className="product-info">
        {product.category && (
          <span className="product-category">{product.category}</span>
        )}
        <h3 className="product-name">{product.name}</h3>
        {product.description && (
          <p className="product-description">{product.description}</p>
        )}

        <div className="product-footer">
          <div className="product-price">
            <span className="price-label">Precio:</span>
            <span className="price-value">${product.price.toFixed(2)}</span>
          </div>

          <motion.button
            className="add-to-cart-btn"
            onClick={handleAddToCart}
            disabled={product.stock_quantity === 0}
            whileTap={{ scale: 0.95 }}
          >
            <FaShoppingCart />
            <span>Agregar</span>
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};
