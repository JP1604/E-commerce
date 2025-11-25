// Custom Hook - useCart
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { container } from '@infrastructure/di/container';
import { CartItem } from '@domain/entities/Cart';

export const useCart = (userId: string) => {
  const queryClient = useQueryClient();

  const cartQuery = useQuery({
    queryKey: ['cart', userId],
    queryFn: () => container.getCartUseCase.execute(userId),
    enabled: !!userId,
  });

  const addItemMutation = useMutation({
    mutationFn: ({ cartId, item }: { cartId: string; item: Omit<CartItem, 'id_item' | 'product_name' | 'id_cart' | 'created_at' | 'updated_at'> }) =>
      container.addItemToCartUseCase.execute(cartId, item),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart', userId] });
    },
  });

  return {
    cart: cartQuery.data,
    isLoading: cartQuery.isLoading,
    error: cartQuery.error,
    addItem: addItemMutation.mutate,
    addItemAsync: addItemMutation.mutateAsync,
    isAddingItem: addItemMutation.isPending,
  };
};
