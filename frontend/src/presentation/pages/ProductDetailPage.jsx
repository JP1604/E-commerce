import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useProduct } from '../hooks/useProducts';
import { useAddToCart, useCart } from '../hooks/useCart';
import { useCartStore } from '../store/cartStore';
import { useUserStore } from '../store/userStore';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card, CardBody } from '../components/ui/Card';

export const ProductDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: product, isLoading } = useProduct(id);
  const { cart } = useCartStore();
  const { isAuthenticated } = useUserStore();
  const addToCart = useAddToCart();
  const [quantity, setQuantity] = useState(1);
  
  // Cargar el carrito si el usuario está autenticado
  useCart();

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      alert('Por favor, inicia sesión para agregar productos al carrito');
      navigate('/login');
      return;
    }

    if (!cart?.id_cart) {
      alert('Espera un momento, estamos preparando tu carrito...');
      setTimeout(() => window.location.reload(), 1000);
      return;
    }

    try {
      await addToCart.mutateAsync({
        cartId: cart.id_cart,
        productId: product.id,
        quantity: quantity,
      });
      alert(`✅ ${product.name} agregado al carrito (${quantity} unidad${quantity > 1 ? 'es' : ''})`);
    } catch (error) {
      console.error('Error adding to cart:', error);
      alert('❌ Error al agregar el producto. Intenta nuevamente.');
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando producto...</p>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="text-center py-12">
        <span className="text-6xl mb-4 block">❌</span>
        <h3 className="text-xl font-semibold text-gray-700 mb-2">Producto no encontrado</h3>
        <Button onClick={() => navigate('/products')} className="mt-4">
          Volver a Productos
        </Button>
      </div>
    );
  }

  const isInStock = product.stock_quantity > 0;

  return (
    <div className="max-w-7xl mx-auto">
      <Button
        variant="outline"
        onClick={() => navigate('/products')}
        className="mb-6"
      >
        ← Volver a Productos
      </Button>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Imagen del Producto */}
        <div className="bg-gradient-to-br from-primary-100 via-secondary-100 to-accent-100 rounded-3xl p-12 flex items-center justify-center shadow-soft">
          <span className="text-9xl">📦</span>
        </div>

        {/* Información del Producto */}
        <div className="space-y-6">
          <div>
            <div className="flex items-center gap-3 mb-3">
              <Badge variant="info" className="text-sm">
                {product.category}
              </Badge>
              <Badge variant={isInStock ? 'success' : 'danger'}>
                {isInStock ? `${product.stock_quantity} en stock` : 'Agotado'}
              </Badge>
            </div>
            <h1 className="text-4xl font-display font-bold text-gray-900 mb-3">
              {product.name}
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed">
              {product.description}
            </p>
          </div>

          <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-2xl p-6">
            <p className="text-sm text-gray-600 mb-2">Precio</p>
            <p className="text-5xl font-bold text-gradient">
              {formatPrice(product.price)}
            </p>
          </div>

          {isInStock && (
            <Card>
              <CardBody>
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  Cantidad
                </label>
                <div className="flex items-center gap-4 mb-4">
                  <Button
                    variant="outline"
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="w-12 h-12"
                  >
                    −
                  </Button>
                  <input
                    type="number"
                    min="1"
                    max={product.stock_quantity}
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(1, Math.min(product.stock_quantity, parseInt(e.target.value) || 1)))}
                    className="w-20 text-center text-xl font-semibold border-2 border-gray-300 rounded-lg py-2"
                  />
                  <Button
                    variant="outline"
                    onClick={() => setQuantity(Math.min(product.stock_quantity, quantity + 1))}
                    className="w-12 h-12"
                  >
                    +
                  </Button>
                  <span className="text-sm text-gray-600">
                    Máximo: {product.stock_quantity}
                  </span>
                </div>
              </CardBody>
            </Card>
          )}

          <Button
            size="lg"
            onClick={handleAddToCart}
            disabled={!isInStock || addToCart.isPending}
            isLoading={addToCart.isPending}
            className="w-full btn-gradient text-lg py-4"
          >
            {addToCart.isPending ? 'Agregando...' : '🛒 Agregar al Carrito'}
          </Button>

          {!isInStock && (
            <p className="text-center text-red-600 font-semibold">
              Este producto está agotado
            </p>
          )}
        </div>
      </div>

      {/* Información Adicional */}
      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardBody className="text-center">
            <div className="text-4xl mb-3">🚚</div>
            <h3 className="font-semibold text-gray-800 mb-2">Envío Gratis</h3>
            <p className="text-sm text-gray-600">En todos tus pedidos</p>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <div className="text-4xl mb-3">🔒</div>
            <h3 className="font-semibold text-gray-800 mb-2">Pago Seguro</h3>
            <p className="text-sm text-gray-600">100% protegido</p>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <div className="text-4xl mb-3">↩️</div>
            <h3 className="font-semibold text-gray-800 mb-2">Devoluciones</h3>
            <p className="text-sm text-gray-600">30 días de garantía</p>
          </CardBody>
        </Card>
      </div>
    </div>
  );
};
