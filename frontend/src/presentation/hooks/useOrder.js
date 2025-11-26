import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { orderRepository } from '../../infrastructure/repositories/OrderRepositoryImpl';
import { useUserStore } from '../store/userStore';
import { useCartStore } from '../store/cartStore';

export const useCreateOrder = () => {
  const queryClient = useQueryClient();
  const { user } = useUserStore();
  const { cart, clearCart, setCart } = useCartStore();

  return useMutation({
    mutationFn: async ({ items, paymentMethod = 'credit_card', deliveryDate, deliveryTimeStart, deliveryTimeEnd }) => {
      if (!user?.id || !cart?.id) {
        throw new Error('Usuario o carrito no disponible');
      }

      const orderData = {
        id_user: user.id,
        id_cart: cart.id,
        items: items.map(item => ({
          id_product: item.product_id || item.id_product,
          quantity: item.quantity,
          unit_price: item.unit_price,
        })),
        payment_method: paymentMethod,
        delivery_date: deliveryDate,
        delivery_time_start: deliveryTimeStart || '09:00',
        delivery_time_end: deliveryTimeEnd || '17:00',
      };

      return await orderRepository.create(orderData);
    },
    onSuccess: async (data) => {
      // Invalidar queries de órdenes
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      queryClient.invalidateQueries({ queryKey: ['orders', user?.id] });
      
      // Limpiar el carrito del store
      clearCart();
      
      // Crear un nuevo carrito automáticamente para futuras compras
      try {
        const { cartRepository } = await import('../../infrastructure/repositories');
        const newCart = await cartRepository.create(user.id, 'activo');
        setCart(newCart);
        console.log('✅ Nuevo carrito creado:', newCart);
      } catch (error) {
        console.error('⚠️ Error creando nuevo carrito:', error);
        // No es crítico si falla, el usuario puede seguir navegando
      }
      
      console.log('✅ Orden creada exitosamente:', data);
    },
    onError: (error) => {
      console.error('❌ Error creando orden:', error);
    },
  });
};

export const useUserOrders = () => {
  const { user } = useUserStore();

  return useQuery({
    queryKey: ['orders', user?.id],
    queryFn: () => {
      if (!user?.id) throw new Error('No user ID');
      return orderRepository.getByUserId(user.id);
    },
    enabled: !!user?.id,
  });
};

export const useOrder = (orderId) => {
  return useQuery({
    queryKey: ['orders', orderId],
    queryFn: () => orderRepository.getById(orderId),
    enabled: !!orderId,
  });
};
