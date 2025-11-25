import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Header } from '@presentation/components/Header/Header';
import { Chatbot } from '@presentation/components/Chatbot/Chatbot';
import { LandingPage } from '@presentation/pages/LandingPage/LandingPage';
import { RegisterPage } from '@presentation/pages/RegisterPage/RegisterPage';
import { LoginPage } from '@presentation/pages/LoginPage/LoginPage';
import { ProductDetailPage } from '@presentation/pages/ProductDetailPage/ProductDetailPage';
import './index.css';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  // TODO: Replace with real user ID from authentication
  const userId = '113a034d-7133-40b6-a4e8-a541a9905297';

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="app">
          <Header />
          
          <main>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/product/:id" element={<ProductDetailPage />} />
              {/* Add more routes here */}
            </Routes>
          </main>

          {/* Chatbot Widget - Always visible */}
          <Chatbot userId={userId} />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
