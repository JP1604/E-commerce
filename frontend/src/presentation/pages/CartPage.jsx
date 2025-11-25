import React, { useState } from 'react';
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

  const [pendingItemId, setPendingItemId] = useState(null);

  const handleUpdateQuantity = async (itemId, quantity) => {
    if (!cart?.id_cart) return;
    console.log('[CartPage] handleUpdateQuantity', { cartId: cart.id_cart, itemId, quantity });
    setPendingItemId(itemId);
    try {
      // optimistic UI: update store before waiting for response
      // this will immediately reflect quantity change while awaiting server
      await updateCartItem.mutateAsync({
        cartId: cart.id_cart,
        itemId,
        quantity,
      });
    } catch (error) {
      console.error('Error updating quantity:', error);
      alert('❌ Error al actualizar la cantidad. Intenta de nuevo.');
    }
    finally {
      setPendingItemId(null);
    }
  };

  const handleRemove = async (itemId) => {
    if (!cart?.id_cart) return;
    
    if (window.confirm('¿Estás seguro de que quieres eliminar este producto?')) {
      console.log('[CartPage] Deleting item:', itemId, 'from cart', cart.id_cart);
      setPendingItemId(itemId);
      try {
        // No optimistic update: remove is immediate on success
        await removeFromCart.mutateAsync({
          cartId: cart.id_cart,
          itemId,
        });
      } catch (error) {
        console.error('Error removing item:', error);
        alert('❌ Error al eliminar el producto. Intenta de nuevo.');
      }
      finally {
        setPendingItemId(null);
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

  const isBusy = updateCartItem.isPending || removeFromCart.isPending;

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
              isUpdating={updateCartItem.isPending && pendingItemId === item.id}
              isRemoving={removeFromCart.isPending && pendingItemId === item.id}
            />
          ))}
        </div>

        <div>
          <CartSummary
            total={total}
            itemCount={itemCount}
            onCheckout={handleCheckout}
            isLoading={isBusy}
          />
        </div>
      </div>
    </div>
  );
};
