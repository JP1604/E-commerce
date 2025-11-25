// Use Case - Get Product By ID
import { Product } from '@domain/entities/Product';
import { IProductRepository } from '@domain/repositories/IProductRepository';

export class GetProductByIdUseCase {
  constructor(private productRepository: IProductRepository) {}

  async execute(id: string): Promise<Product> {
    return await this.productRepository.getById(id);
  }
}
