// Domain Entity - Product
export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock_quantity: number;
  category: string;
  image_url?: string;
  created_at: string;
  updated_at: string;
}

export interface ProductFilters {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  search?: string;
}
