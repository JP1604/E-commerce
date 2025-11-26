/**
 * @typedef {'creada' | 'pagada' | 'enviada' | 'entregada' | 'cancelada'} OrderStatus
 */

/**
 * @typedef {Object} OrderItem
 * @property {string} id
 * @property {string} product_id
 * @property {number} quantity
 * @property {number} unit_price
 * @property {number} subtotal
 */

/**
 * @typedef {Object} Order
 * @property {string} id
 * @property {string} user_id
 * @property {string} cart_id
 * @property {number} total
 * @property {OrderStatus} status
 * @property {string} [payment_id]
 * @property {OrderItem[]} items
 * @property {string} created_at
 * @property {string} [updated_at]
 */

export const ORDER_STATUS = {
  CREATED: 'creada',
  PAID: 'pagada',
  SHIPPED: 'enviada',
  DELIVERED: 'entregada',
  CANCELLED: 'cancelada',
};

export const createOrder = (data) => ({
  id: data.id || data.id_order,
  user_id: data.user_id || data.id_user,
  cart_id: data.cart_id || data.id_cart,
  total: data.total,
  status: data.status,
  payment_id: data.payment_id,
  items: (data.items || []).map(item => createOrderItem(item)),
  created_at: data.created_at,
  updated_at: data.updated_at,
});

export const createOrderItem = (data) => ({
  id: data.id || data.id_order_item,
  product_id: data.product_id || data.id_product,
  quantity: data.quantity,
  unit_price: data.unit_price,
  subtotal: data.subtotal,
});
