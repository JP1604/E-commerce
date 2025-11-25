// Product Detail Page - Modern Design
import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { container } from '@infrastructure/di/container';
import { useCart } from '@presentation/hooks/useCart';
import { motion } from 'framer-motion';
import { 
  FaShoppingCart, 
  FaArrowLeft, 
  FaMinus, 
  FaPlus, 
  FaCheck,
  FaBox,
  FaTruck,
  FaShieldAlt
} from 'react-icons/fa';
import './ProductDetailPage.css';

export const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const userId = localStorage.getItem('userId') || '113a034d-7133-40b6-a4e8-a541a9905297';
  
  const [quantity, setQuantity] = useState(1);
  const [addedToCart, setAddedToCart] = useState(false);

  const { data: product, isLoading, error } = useQuery({
    queryKey: ['product', id],
    queryFn: () => container.getProductByIdUseCase.execute(id!),
    enabled: !!id,
  });

  const { cart, addItem, isAddingItem } = useCart(userId);

  const handleQuantityChange = (change: number) => {
    const newQuantity = quantity + change;
    if (newQuantity >= 1 && product && newQuantity <= product.stock_quantity) {
      setQuantity(newQuantity);
    }
  };

  const handleAddToCart = () => {
    if (!product || !cart) return;

    addItem(
      {
        cartId: cart.id_cart,
        item: {
          product_id: product.id,
          quantity: quantity,
          price: product.price,
        },
      },
      {
        onSuccess: () => {
          setAddedToCart(true);
          setTimeout(() => setAddedToCart(false), 3000);
        },
      }
    );
  };

  if (isLoading) {
    return (
      <div className="product-detail-page loading-state">
        <div className="spinner-large"></div>
        <p>Cargando producto...</p>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="product-detail-page error-state">
        <div className="error-content">
          <h2>⚠️ Producto no encontrado</h2>
          <p>El producto que buscas no existe o no está disponible.</p>
          <button onClick={() => navigate('/')} className="back-button">
            <FaArrowLeft /> Volver al inicio
          </button>
        </div>
      </div>
    );
  }

  const isOutOfStock = product.stock_quantity === 0;
  const isLowStock = product.stock_quantity < 10 && product.stock_quantity > 0;

  return (
    <div className="product-detail-page">
      <div className="product-detail-container">
        {/* Back Button */}
        <motion.button
          className="back-btn"
          onClick={() => navigate(-1)}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <FaArrowLeft /> Volver
        </motion.button>

        <div className="product-detail-grid">
          {/* Product Image */}
          <motion.div
            className="product-image-section"
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="product-image-main">
              {product.image_url ? (
                <img src={product.image_url} alt={product.name} />
              ) : (
                <div className="image-placeholder">
                  <FaBox />
                  <p>Sin imagen disponible</p>
                </div>
              )}
            </div>

            {/* Trust Badges */}
            <div className="trust-badges">
              <div className="badge">
                <FaTruck />
                <span>Envío rápido</span>
              </div>
              <div className="badge">
                <FaShieldAlt />
                <span>Compra segura</span>
              </div>
              <div className="badge">
                <FaCheck />
                <span>Garantía</span>
              </div>
            </div>
          </motion.div>

          {/* Product Info */}
          <motion.div
            className="product-info-section"
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            {/* Category */}
            {product.category && (
              <span className="product-category-badge">{product.category}</span>
            )}

            {/* Name */}
            <h1 className="product-title">{product.name}</h1>

            {/* Price */}
            <div className="product-price-section">
              <span className="price-label">Precio:</span>
              <span className="price-value">${product.price.toFixed(2)}</span>
            </div>

            {/* Stock Status */}
            <div className="stock-status">
              {isOutOfStock ? (
                <span className="status-badge out-of-stock">
                  ❌ Agotado
                </span>
              ) : isLowStock ? (
                <span className="status-badge low-stock">
                  ⚠️ Solo {product.stock_quantity} disponibles
                </span>
              ) : (
                <span className="status-badge in-stock">
                  ✅ Disponible ({product.stock_quantity} en stock)
                </span>
              )}
            </div>

            {/* Description */}
            <div className="product-description">
              <h3>Descripción</h3>
              <p>{product.description || 'Sin descripción disponible.'}</p>
            </div>

            {/* Quantity Selector & Add to Cart */}
            {!isOutOfStock && (
              <div className="purchase-section">
                <div className="quantity-selector">
                  <span className="quantity-label">Cantidad:</span>
                  <div className="quantity-controls">
                    <button
                      onClick={() => handleQuantityChange(-1)}
                      disabled={quantity <= 1}
                      className="quantity-btn"
                    >
                      <FaMinus />
                    </button>
                    <span className="quantity-value">{quantity}</span>
                    <button
                      onClick={() => handleQuantityChange(1)}
                      disabled={quantity >= product.stock_quantity}
                      className="quantity-btn"
                    >
                      <FaPlus />
                    </button>
                  </div>
                </div>

                <motion.button
                  className={`add-to-cart-button ${addedToCart ? 'success' : ''}`}
                  onClick={handleAddToCart}
                  disabled={isAddingItem || addedToCart}
                  whileTap={{ scale: 0.98 }}
                >
                  {addedToCart ? (
                    <>
                      <FaCheck /> Agregado al carrito
                    </>
                  ) : isAddingItem ? (
                    <>
                      <span className="spinner-small"></span>
                      Agregando...
                    </>
                  ) : (
                    <>
                      <FaShoppingCart /> Agregar al carrito
                    </>
                  )}
                </motion.button>
              </div>
            )}

            {/* Total */}
            {!isOutOfStock && (
              <div className="total-section">
                <span>Total:</span>
                <span className="total-price">
                  ${(product.price * quantity).toFixed(2)}
                </span>
              </div>
            )}

            {/* Product Details */}
            <div className="product-details">
              <h3>Detalles del producto</h3>
              <ul>
                <li>
                  <strong>SKU:</strong> {product.id.substring(0, 8).toUpperCase()}
                </li>
                <li>
                  <strong>Categoría:</strong> {product.category || 'General'}
                </li>
                <li>
                  <strong>Stock disponible:</strong> {product.stock_quantity} unidades
                </li>
                <li>
                  <strong>Fecha de publicación:</strong>{' '}
                  {new Date(product.created_at).toLocaleDateString('es-ES')}
                </li>
              </ul>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};
