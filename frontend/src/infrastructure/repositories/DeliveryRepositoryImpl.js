import { deliveryApi } from '../api/apiClient';

export class DeliveryRepositoryImpl {
  async create(deliveryData) {
    const response = await deliveryApi.post('/deliveries/', deliveryData);
    return response.data;
  }

  async getById(deliveryId) {
    const response = await deliveryApi.get(`/deliveries/${deliveryId}`);
    return response.data;
  }

  async getByOrderId(orderId) {
    const response = await deliveryApi.get(`/deliveries/order/${orderId}`);
    return response.data;
  }

  async updateStatus(deliveryId, status) {
    const response = await deliveryApi.patch(`/deliveries/${deliveryId}`, { status });
    return response.data;
  }
}

export const deliveryRepository = new DeliveryRepositoryImpl();
