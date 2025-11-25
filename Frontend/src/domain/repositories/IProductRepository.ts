// Domain Repository Interface - Products
import { Product, ProductFilters } from '../entities/Product';

export interface IProductRepository {
  getAll(filters?: ProductFilters): Promise<Product[]>;
  getById(id: string): Promise<Product>;
  search(query: string): Promise<Product[]>;
}
