/**
 * @typedef {Object} CartItem
 * @property {string} id
 * @property {string} cart_id
 * @property {string} product_id
 * @property {number} quantity
 * @property {number} unit_price
 * @property {number} subtotal
 */

/**
 * @typedef {Object} Cart
 * @property {string} id
 * @property {string} user_id
 * @property {string} status
 * @property {CartItem[]} [items]
 * @property {string} [created_at]
 */

export const createCart = (data) => ({
  id: data.id || data.id_cart,
  // preserve legacy server field name for compatibility with frontend that uses id_cart
  id_cart: data.id_cart || data.id,
  user_id: data.user_id || data.id_user,
  status: data.status,
  items: data.items || [],
  created_at: data.created_at,
});

export const createCartItem = (data) => ({
  id: data.id || data.id_cart_item,
  // preserve legacy server field names for compatibility
  id_cart_item: data.id_cart_item || data.id,
  cart_id: data.cart_id || data.id_cart,
  product_id: data.product_id || data.id_product,
  quantity: data.quantity,
  unit_price: data.unit_price,
  subtotal: data.subtotal,
});
