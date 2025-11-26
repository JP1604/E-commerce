import { productApi } from '../api/apiClient';
import { createProduct } from '../../domain/entities/Product';

export class ProductRepositoryImpl {
  async getAll() {
    const response = await productApi.get('/products/');
    return response.data.map(createProduct);
  }

  async getById(id) {
    const response = await productApi.get(`/products/${id}`);
    return createProduct(response.data);
  }

  async create(product) {
    const response = await productApi.post('/products/', product);
    return createProduct(response.data);
  }

  async update(id, product) {
    const response = await productApi.put(`/products/${id}`, product);
    return createProduct(response.data);
  }

  async delete(id) {
    await productApi.delete(`/products/${id}`);
  }
}

export const productRepository = new ProductRepositoryImpl();
