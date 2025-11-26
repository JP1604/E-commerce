import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './presentation/components/layout/Layout';
import { HomePage } from './presentation/pages/HomePage';
import { ProductsPage } from './presentation/pages/ProductsPage';
import { ProductDetailPage } from './presentation/pages/ProductDetailPage';
import { CartPage } from './presentation/pages/CartPage';
import { CheckoutPage } from './presentation/pages/CheckoutPage';
import { DeliveryPage } from './presentation/pages/DeliveryPage';
import { LoginPage } from './presentation/pages/LoginPage';
import { RegisterPage } from './presentation/pages/RegisterPage';
import { AddProductPage } from './presentation/pages/AddProductPage';
import { useUserStore } from './presentation/store/userStore';
import { useCart } from './presentation/hooks/useCart';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useUserStore();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// Cart Initializer - Load cart when user is authenticated
const CartInitializer = () => {
  useCart(); // This will automatically fetch cart when user is logged in
  return null;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <CartInitializer />
        <Routes>
          {/* Public Routes without Layout */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* Routes with Layout */}
          <Route path="/" element={
            <Layout>
              <HomePage />
            </Layout>
          } />
          
          <Route path="/products" element={
            <Layout>
              <ProductsPage />
            </Layout>
          } />
          
          <Route path="/products/:id" element={
            <Layout>
              <ProductDetailPage />
            </Layout>
          } />
          
          <Route path="/sell-products" element={
            <ProtectedRoute>
              <Layout>
                <AddProductPage />
              </Layout>
            </ProtectedRoute>
          } />
          
          {/* Protected Routes */}
          <Route path="/cart" element={
            <ProtectedRoute>
              <Layout>
                <CartPage />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/checkout" element={
            <ProtectedRoute>
              <Layout>
                <CheckoutPage />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/delivery/:orderId" element={
            <ProtectedRoute>
              <Layout>
                <DeliveryPage />
              </Layout>
            </ProtectedRoute>
          } />
          
          {/* Redirect unknown routes */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
