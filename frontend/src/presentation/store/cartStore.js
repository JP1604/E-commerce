import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useCartStore = create(
  persist(
    (set, get) => ({
      cart: null,
      items: [],
      isLoading: false,

      setCart: (cart) => set({ cart }),
      
      setItems: (items) => set({ items }),
      
      addItem: (item) => set((state) => {
        const existingItem = state.items.find(i => i.product_id === item.product_id);
        if (existingItem) {
          return {
            items: state.items.map(i =>
              i.product_id === item.product_id
                ? { ...i, quantity: i.quantity + item.quantity, subtotal: (i.quantity + item.quantity) * i.unit_price }
                : i
            ),
          };
        }
        return { items: [...state.items, item] };
      }),
      
      removeItem: (itemId) => set((state) => ({
        items: state.items.filter((i) => i.id !== itemId),
      })),
      
      updateItemQuantity: (itemId, quantity) => set((state) => ({
        items: state.items.map((i) =>
          i.id === itemId ? { ...i, quantity, subtotal: i.unit_price * quantity } : i
        ),
      })),
      
      clearCart: () => set({ items: [], cart: null }),
      
      setLoading: (isLoading) => set({ isLoading }),

      getTotal: () => {
        const state = get();
        return state.items.reduce((sum, item) => sum + item.subtotal, 0);
      },

      getItemCount: () => {
        const state = get();
        return state.items.reduce((sum, item) => sum + item.quantity, 0);
      },
    }),
    {
      name: 'cart-storage',
    }
  )
);
