import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';
import { useUserStore } from '../store/userStore';
import { useCart, useRemoveFromCart, useUpdateCartItem } from '../hooks/useCart';
import { Button } from '../components/ui/Button';
import { CartItem } from '../components/cart/CartItem';
import { CartSummary } from '../components/cart/CartSummary';

export const CartPage = () => {
  const { cart, items } = useCartStore();
  const { user } = useUserStore();
  const { isLoading: cartLoading } = useCart();
  const removeFromCart = useRemoveFromCart();
  const updateCartItem = useUpdateCartItem();
  const navigate = useNavigate();

  const total = items.reduce((sum, item) => sum + item.subtotal, 0);
  const itemCount = items.length;

  const handleUpdateQuantity = async (itemId, quantity) => {
    if (!cart?.id_cart) return;
    
    try {
      await updateCartItem.mutateAsync({
        cartId: cart.id_cart,
        itemId,
        quantity,
      });
    } catch (error) {
      console.error('Error updating quantity:', error);
    }
  };

  const handleRemove = async (itemId) => {
    if (!cart?.id_cart) return;
    
    if (window.confirm('¿Estás seguro de que quieres eliminar este producto?')) {
      try {
        await removeFromCart.mutateAsync({
          cartId: cart.id_cart,
          itemId,
        });
      } catch (error) {
        console.error('Error removing item:', error);
      }
    }
  };

  const handleCheckout = () => {
    navigate('/checkout');
  };

  if (cartLoading) {
    return (
      <div className="text-center py-16">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Cargando carrito...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="text-center py-16">
        <span className="text-8xl mb-6 block">🔒</span>
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Inicia sesión para ver tu carrito</h2>
        <Link to="/login">
          <Button variant="primary" size="lg">Iniciar Sesión</Button>
        </Link>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="text-center py-16">
        <span className="text-8xl mb-6 block">🛒</span>
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Tu carrito está vacío</h2>
        <p className="text-gray-600 mb-8">¡Agrega algunos productos para comenzar!</p>
        <Link to="/products">
          <Button variant="primary" size="lg">Ver Productos</Button>
        </Link>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Mi Carrito ({itemCount} productos)</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
          {items.map((item) => (
            <CartItem
              key={item.id}
              item={item}
              onUpdateQuantity={handleUpdateQuantity}
              onRemove={handleRemove}
            />
          ))}
        </div>

        <div>
          <CartSummary
            total={total}
            itemCount={itemCount}
            onCheckout={handleCheckout}
          />
        </div>
      </div>
    </div>
  );
};
