import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { productRepository } from '../../infrastructure/repositories';

export const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: () => productRepository.getAll(),
    staleTime: 1000 * 60 * 5,
  });
};

export const useProduct = (id) => {
  return useQuery({
    queryKey: ['product', id],
    queryFn: () => productRepository.getById(id),
    enabled: !!id,
  });
};

export const useCreateProduct = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (product) => productRepository.create(product),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
};

export const useUpdateProduct = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...product }) => productRepository.update(id, product),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
};

export const useDeleteProduct = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => productRepository.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
};
