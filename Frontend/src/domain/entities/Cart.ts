// Domain Entity - Cart
export interface CartItem {
  id_item: string;
  id_cart: string;
  product_id: string;
  quantity: number;
  price: number;
  product_name?: string;
  created_at: string;
  updated_at: string;
}

export interface Cart {
  id_cart: string;
  user_id: string;
  status: 'activo' | 'vacio' | 'abandonado';
  items?: CartItem[];
  created_at: string;
  updated_at: string;
}
