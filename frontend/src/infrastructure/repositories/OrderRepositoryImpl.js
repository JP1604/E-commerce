import { orderApi } from '../api/apiClient';
import { createOrder } from '../../domain/entities/Order';

export class OrderRepositoryImpl {
  async getAll() {
    const response = await orderApi.get('/orders/');
    return response.data.map(createOrder);
  }

  async getById(id) {
    const response = await orderApi.get(`/orders/${id}`);
    return createOrder(response.data);
  }

  async getByUserId(userId) {
    const response = await orderApi.get(`/orders/user/${userId}`);
    return response.data.map(createOrder);
  }

  async create(orderData) {
    const response = await orderApi.post('/orders/', orderData);
    return createOrder(response.data);
  }

  async updateStatus(id, status) {
    const response = await orderApi.patch(`/orders/${id}`, { status });
    return createOrder(response.data);
  }
}

export const orderRepository = new OrderRepositoryImpl();
