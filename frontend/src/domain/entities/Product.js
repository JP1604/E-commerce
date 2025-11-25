/**
 * @typedef {Object} Product
 * @property {string} id
 * @property {string} name
 * @property {string} description
 * @property {number} price
 * @property {string} category
 * @property {number} stock_quantity
 * @property {string} [created_at]
 * @property {string} [updated_at]
 */

export const createProduct = (data) => ({
  id: data.id || data.id_product,
  name: data.name,
  description: data.description,
  price: data.price,
  category: data.category,
  stock_quantity: data.stock_quantity,
  created_at: data.created_at,
  updated_at: data.updated_at,
});
