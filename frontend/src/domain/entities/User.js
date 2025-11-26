/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} name
 * @property {string} email
 * @property {string} [address]
 * @property {string} [phone]
 * @property {string} [created_at]
 */

export const createUser = (data) => ({
  id: data.id || data.id_user,
  name: data.name,
  email: data.email,
  address: data.address,
  phone: data.phone,
  created_at: data.created_at,
});
