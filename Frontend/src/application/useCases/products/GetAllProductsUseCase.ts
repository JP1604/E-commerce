// Use Case - Get All Products
import { Product, ProductFilters } from '@domain/entities/Product';
import { IProductRepository } from '@domain/repositories/IProductRepository';

export class GetAllProductsUseCase {
  constructor(private productRepository: IProductRepository) {}

  async execute(filters?: ProductFilters): Promise<Product[]> {
    return await this.productRepository.getAll(filters);
  }
}
