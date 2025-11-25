// Custom Hook - useProducts
import { useQuery } from '@tanstack/react-query';
import { container } from '@infrastructure/di/container';
import { ProductFilters } from '@domain/entities/Product';

export const useProducts = (filters?: ProductFilters) => {
  return useQuery({
    queryKey: ['products', filters],
    queryFn: () => container.getAllProductsUseCase.execute(filters),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};
