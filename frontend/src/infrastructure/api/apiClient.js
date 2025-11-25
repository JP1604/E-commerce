import axios from 'axios';

const API_URLS = {
  products: import.meta.env.VITE_PRODUCT_SERVICE_URL || 'http://localhost:8000',
  users: import.meta.env.VITE_USER_SERVICE_URL || 'http://localhost:8001',
  delivery: import.meta.env.VITE_DELIVERY_SERVICE_URL || 'http://localhost:8002',
  cart: import.meta.env.VITE_CART_SERVICE_URL || 'http://localhost:8003',
  orders: import.meta.env.VITE_ORDER_SERVICE_URL || 'http://localhost:8005',
  validation: import.meta.env.VITE_VALIDATION_SERVICE_URL || 'http://localhost:8006',
  payments: import.meta.env.VITE_PAYMENT_SERVICE_URL || 'http://localhost:8007',
};

const createApiClient = (baseURL) => {
  const client = axios.create({
    baseURL: `${baseURL}/api/v1`,
    headers: { 'Content-Type': 'application/json' },
    timeout: 10000,
  });

  // Interceptor para agregar token de autenticación
  client.interceptors.request.use(
    (config) => {
      const userStorage = localStorage.getItem('user-storage');
      if (userStorage) {
        try {
          const { state } = JSON.parse(userStorage);
          if (state?.user?.id) {
            config.headers['X-User-ID'] = state.user.id;
          }
        } catch (error) {
          console.error('Error parsing user storage:', error);
        }
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Interceptor para manejo de errores
  client.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response) {
        console.error('API Error:', error.response.data);
      } else if (error.request) {
        console.error('Network Error:', error.message);
      }
      return Promise.reject(error);
    }
  );

  return client;
};

export const productApi = createApiClient(API_URLS.products);
export const userApi = createApiClient(API_URLS.users);
export const deliveryApi = createApiClient(API_URLS.delivery);
export const cartApi = createApiClient(API_URLS.cart);
export const orderApi = createApiClient(API_URLS.orders);
export const validationApi = createApiClient(API_URLS.validation);
export const paymentApi = createApiClient(API_URLS.payments);

export default API_URLS;
