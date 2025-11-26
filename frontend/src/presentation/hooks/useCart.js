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
  const { user } = useUserStore();

  return useMutation({
    mutationFn: ({ cartId, productId, quantity }) =>
      cartRepository.addItem(cartId, productId, quantity),
    onSuccess: (data) => {
      addItem(data);
      // invalidate the correct cart query for the current user
      queryClient.invalidateQueries({ queryKey: ['cart', user?.id] });
    },
  });
};

export const useRemoveFromCart = () => {
  const queryClient = useQueryClient();
  const { removeItem } = useCartStore();
  const { user } = useUserStore();

  return useMutation({
    mutationFn: ({ cartId, itemId }) => cartRepository.removeItem(cartId, itemId),
    onMutate: async ({ itemId }) => {
      console.log('[useRemoveFromCart] onMutate itemId:', itemId);
      // Optimistically remove from store and keep previous state for rollback
      const previousItems = useCartStore.getState().items;
      removeItem(itemId);
      return { previousItems };
    },
    onError: (err, variables, context) => {
      console.error('Error removing item:', err);
      if (context?.previousItems) {
        useCartStore.getState().setItems(context.previousItems);
      }
    },
    onSuccess: (data, { itemId }) => {
      console.log('[useRemoveFromCart] onSuccess itemId:', itemId, 'response:', data);
      // Remove item from store (fallback in case onMutate didn't persist to UI due to refetch)
      removeItem(itemId);
      // Invalidate the correct cart query to reload fresh data
      queryClient.invalidateQueries({ queryKey: ['cart', user?.id] });
    },
    onSettled: () => {
      // Ensure we always refresh the cart when mutation finishes
      queryClient.invalidateQueries({ queryKey: ['cart', user?.id] });
    },
  });
};

export const useUpdateCartItem = () => {
  const queryClient = useQueryClient();
  const { updateItemQuantity } = useCartStore();
  const { user } = useUserStore();

  return useMutation({
    mutationFn: ({ cartId, itemId, quantity }) =>
      cartRepository.updateItem(cartId, itemId, quantity),
    onMutate: ({ itemId, quantity }) => {
      const previousItems = useCartStore.getState().items;
      // update optimistically
      updateItemQuantity(itemId, quantity);
      return { previousItems };
    },
    onError: (err, variables, context) => {
      console.error('Error updating item quantity:', err);
      if (context?.previousItems) {
        useCartStore.getState().setItems(context.previousItems);
      }
    },
    onSuccess: (data) => {
      console.log('Updated item response:', data);
      updateItemQuantity(data.id, data.quantity);
      // refresh the specific user's cart query
      queryClient.invalidateQueries({ queryKey: ['cart', user?.id] });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['cart', user?.id] });
    },
  });
};
