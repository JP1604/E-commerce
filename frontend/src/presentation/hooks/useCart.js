import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { cartRepository } from '../../infrastructure/repositories';
import { useCartStore } from '../store/cartStore';
import { useUserStore } from '../store/userStore';

export const useCart = () => {
  const { user } = useUserStore();
  const { setCart, setItems } = useCartStore();

  return useQuery({
    queryKey: ['cart', user?.id],
    queryFn: async () => {
      if (!user?.id) {
        console.log('❌ No user ID found');
        throw new Error('No user logged in');
      }
      console.log('🔍 Buscando carrito para usuario:', user.id);
      try {
        const cart = await cartRepository.getByUserId(user.id);
        console.log('✅ Carrito encontrado:', cart);
        const items = await cartRepository.getItems(cart.id); // Usar 'id' en lugar de 'id_cart'
        console.log('📦 Items del carrito:', items);
        setCart(cart);
        setItems(items);
        return { cart, items };
      } catch (error) {
        console.log('⚠️ Error al obtener carrito:', error.response?.status, error.message);
        // Si no existe carrito, crear uno nuevo
        if (error.response?.status === 404) {
          console.log('🆕 Creando nuevo carrito para usuario:', user.id);
          const newCart = await cartRepository.create(user.id);
          console.log('✅ Nuevo carrito creado:', newCart);
          setCart(newCart);
          setItems([]);
          return { cart: newCart, items: [] };
        }
        throw error;
      }
    },
    enabled: !!user?.id,
    retry: false,
  });
};

export const useAddToCart = () => {
  const queryClient = useQueryClient();
  const { addItem } = useCartStore();

  return useMutation({
    mutationFn: ({ cartId, productId, quantity }) =>
      cartRepository.addItem(cartId, productId, quantity),
    onSuccess: (data) => {
      addItem(data);
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
};

export const useRemoveFromCart = () => {
  const queryClient = useQueryClient();
  const { removeItem } = useCartStore();

  return useMutation({
    mutationFn: ({ cartId, itemId }) => cartRepository.removeItem(cartId, itemId),
    onSuccess: (_, { itemId }) => {
      removeItem(itemId);
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
};

export const useUpdateCartItem = () => {
  const queryClient = useQueryClient();
  const { updateItemQuantity } = useCartStore();

  return useMutation({
    mutationFn: ({ cartId, itemId, quantity }) =>
      cartRepository.updateItem(cartId, itemId, quantity),
    onSuccess: (data) => {
      updateItemQuantity(data.id, data.quantity);
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
};
