import { useQuery, useMutation, useQueryClient } from '@tantml:react-query';
import { orderRepository } from '../../infrastructure/repositories';

export const useOrders = () => {
  return useQuery({
    queryKey: ['orders'],
    queryFn: () => orderRepository.getAll(),
  });
};

export const useUserOrders = (userId) => {
  return useQuery({
    queryKey: ['orders', 'user', userId],
    queryFn: () => orderRepository.getByUserId(userId),
    enabled: !!userId,
  });
};

export const useCreateOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (orderData) => orderRepository.create(orderData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
};
