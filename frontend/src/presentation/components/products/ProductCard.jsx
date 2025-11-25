import React from 'react';
import { Card, CardBody, CardFooter } from '../ui/Card';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { useAddToCart, useCart } from '../../hooks/useCart';
import { useCartStore } from '../../store/cartStore';
import { useUserStore } from '../../store/userStore';
import { useNavigate } from 'react-router-dom';
import { cartRepository } from '../../../infrastructure/repositories';

export const ProductCard = ({ product, onViewDetails }) => {
  const { cart } = useCartStore();
  const { user, isAuthenticated } = useUserStore();
  const addToCart = useAddToCart();
  const navigate = useNavigate();
  
  // Log para depuración
  React.useEffect(() => {
    console.log('📊 ProductCard Estado:', { isAuthenticated, user: user?.id, cartId: cart?.id });
  }, [isAuthenticated, user, cart]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const isInStock = product.stock_quantity > 0;

  const handleAddToCart = async (e) => {
    // Prevenir que el click propague al card (evita navegación)
    e.stopPropagation();
    
    console.log('🛒 Intentando agregar al carrito');
    console.log('👤 Usuario autenticado:', isAuthenticated, 'User ID:', user?.id);
    console.log('🛍️ Carrito actual:', cart);
    
    if (!isAuthenticated || !user?.id) {
      alert('Por favor, inicia sesión para agregar productos al carrito');
      navigate('/login');
      return;
    }

    try {
      let cartId = cart?.id; // Usar 'id' en lugar de 'id_cart'
      
      // Si no hay carrito, crear uno nuevo
      if (!cartId) {
        console.log('🆕 Creando carrito nuevo para usuario:', user.id);
        const newCart = await cartRepository.create(user.id);
        console.log('✅ Carrito creado:', newCart);
        cartId = newCart.id; // Usar 'id' en lugar de 'id_cart'
        
        // Actualizar el store
        useCartStore.getState().setCart(newCart);
      }

      console.log('✅ Carrito listo, agregando producto:', product.id, 'al carrito:', cartId);
      const result = await addToCart.mutateAsync({
        cartId: cartId,
        productId: product.id,
        quantity: 1,
      });
      console.log('✅ Producto agregado exitosamente:', result);
      alert(`✅ ${product.name} agregado al carrito`);
    } catch (error) {
      console.error('❌ Error completo:', error);
      alert(`❌ Error: ${error.message || 'No se pudo agregar el producto'}`);
    }
  };

  return (
    <Card className="hover:shadow-xl transition-all duration-300 h-full flex flex-col group">
      <div 
        className="h-48 bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center cursor-pointer group-hover:scale-105 transition-transform duration-300"
        onClick={() => navigate(`/products/${product.id}`)}
      >
        <span className="text-6xl">📦</span>
      </div>
      <CardBody className="flex-1 flex flex-col">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-lg font-bold text-gray-800 truncate flex-1">{product.name}</h3>
          <Badge variant="info" className="ml-2 flex-shrink-0">
            {product.category}
          </Badge>
        </div>
        <p className="text-gray-600 text-sm mb-3 line-clamp-2 flex-1">{product.description}</p>
        <div className="flex items-center justify-between mt-auto">
          <span className="text-2xl font-bold text-blue-600">{formatPrice(product.price)}</span>
          <Badge variant={isInStock ? 'success' : 'danger'}>
            {isInStock ? `${product.stock_quantity} en stock` : 'Agotado'}
          </Badge>
        </div>
      </CardBody>
      <CardFooter>
        <Button
          variant="primary"
          className="w-full"
          onClick={handleAddToCart}
          disabled={!isInStock || addToCart.isPending}
          isLoading={addToCart.isPending}
        >
          {addToCart.isPending ? 'Agregando...' : '🛒 Agregar al carrito'}
        </Button>
      </CardFooter>
    </Card>
  );
};
