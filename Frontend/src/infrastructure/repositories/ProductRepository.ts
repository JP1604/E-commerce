// Product Repository Implementation
import { Product, ProductFilters } from '@domain/entities/Product';
import { IProductRepository } from '@domain/repositories/IProductRepository';
import { apiClient } from '../http/httpClient';

export class ProductRepository implements IProductRepository {
  private readonly basePath = '/api/v1/products/';

  async getAll(filters?: ProductFilters): Promise<Product[]> {
    // Backend returns all products, apply client-side filtering
    const response = await apiClient.get<Product[]>(this.basePath);
    let products = response.data;
    
    // Apply client-side filtering if needed
    if (filters?.search) {
      const searchLower = filters.search.toLowerCase();
      products = products.filter(p => 
        p.name.toLowerCase().includes(searchLower) ||
        p.description.toLowerCase().includes(searchLower)
      );
    }
    
    if (filters?.category) {
      products = products.filter(p => p.category === filters.category);
    }
    
    if (filters?.minPrice) {
      products = products.filter(p => p.price >= filters.minPrice!);
    }
    
    if (filters?.maxPrice) {
      products = products.filter(p => p.price <= filters.maxPrice!);
    }
    
    return products;
  }

  async getById(id: string): Promise<Product> {
    const response = await apiClient.get<Product>(`${this.basePath}${id}`);
    return response.data;
  }

  async search(query: string): Promise<Product[]> {
    const response = await apiClient.get<Product[]>(
      `${this.basePath}?search=${encodeURIComponent(query)}`
    );
    return response.data;
  }
}
