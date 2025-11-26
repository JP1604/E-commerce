import React from 'react';
import { Link } from 'react-router-dom';
import { useProducts } from '../hooks/useProducts';
import { useCart } from '../hooks/useCart';
import { ProductGrid } from '../components/products/ProductGrid';
import { Button } from '../components/ui/Button';
import { Card, CardBody } from '../components/ui/Card';

export const HomePage = () => {
  const { data: products, isLoading } = useProducts();
  
  // Cargar el carrito si el usuario está autenticado
  useCart();

  const featuredProducts = products?.slice(0, 8) || [];

  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-500/10 via-secondary-500/10 to-accent-500/10 rounded-3xl"></div>
        <div className="relative bg-white/50 backdrop-blur-sm rounded-3xl p-8 md:p-16 shadow-soft">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="inline-block">
                <span className="px-4 py-2 bg-gradient-to-r from-primary-100 to-secondary-100 text-primary-700 rounded-full text-sm font-semibold">
                  ✨ Bienvenido a NovaMarket
                </span>
              </div>
              <h1 className="text-4xl md:text-6xl font-display font-bold text-gray-900 leading-tight">
                El futuro de las
                <span className="block text-gradient">compras online</span>
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed">
                Descubre productos innovadores con la mejor experiencia de compra. 
                Envío gratis en todos tus pedidos y ofertas exclusivas.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/products">
                  <Button size="lg" className="btn-gradient shadow-lg hover:shadow-xl w-full sm:w-auto">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Explorar Productos
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="lg" variant="outline" className="w-full sm:w-auto border-2 border-primary-600 text-primary-600 hover:bg-primary-50">
                    Crear Cuenta Gratis
                  </Button>
                </Link>
              </div>
              <div className="flex items-center space-x-8 pt-4">
                <div>
                  <div className="text-3xl font-bold text-gray-900">10K+</div>
                  <div className="text-sm text-gray-600">Productos</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">50K+</div>
                  <div className="text-sm text-gray-600">Clientes</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">4.9★</div>
                  <div className="text-sm text-gray-600">Valoración</div>
                </div>
              </div>
            </div>
            <div className="relative hidden lg:block">
              <div className="absolute inset-0 bg-gradient-to-r from-primary-400 to-secondary-400 rounded-3xl blur-3xl opacity-20 animate-pulse"></div>
              <div className="relative">
                <div className="grid grid-cols-2 gap-4">
                  {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="aspect-square bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-soft card-hover p-6 flex items-center justify-center">
                      <div className="text-6xl animate-float" style={{ animationDelay: `${i * 0.2}s` }}>
                        {['🎮', '👟', '📱', '🎧'][i - 1]}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Sell Your Products Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-accent-500/10 via-primary-500/10 to-secondary-500/10 rounded-3xl"></div>
        <div className="relative bg-white/60 backdrop-blur-sm rounded-3xl p-8 md:p-12 shadow-soft border-2 border-accent-100">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            <div className="order-2 lg:order-1">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-4">
                  <div className="bg-gradient-to-br from-primary-50 to-primary-100 rounded-2xl p-6 card-hover">
                    <div className="text-4xl mb-2">📦</div>
                    <div className="font-semibold text-gray-900">Sin comisiones</div>
                    <div className="text-sm text-gray-600">Vende sin costos extras</div>
                  </div>
                  <div className="bg-gradient-to-br from-secondary-50 to-secondary-100 rounded-2xl p-6 card-hover">
                    <div className="text-4xl mb-2">⚡</div>
                    <div className="font-semibold text-gray-900">Publicación rápida</div>
                    <div className="text-sm text-gray-600">En segundos</div>
                  </div>
                </div>
                <div className="space-y-4 mt-8">
                  <div className="bg-gradient-to-br from-accent-50 to-accent-100 rounded-2xl p-6 card-hover">
                    <div className="text-4xl mb-2">👥</div>
                    <div className="font-semibold text-gray-900">Miles de compradores</div>
                    <div className="text-sm text-gray-600">Gran audiencia</div>
                  </div>
                  <div className="bg-gradient-to-br from-primary-50 to-secondary-100 rounded-2xl p-6 card-hover">
                    <div className="text-4xl mb-2">💰</div>
                    <div className="font-semibold text-gray-900">Pagos seguros</div>
                    <div className="text-sm text-gray-600">100% protegidos</div>
                  </div>
                </div>
              </div>
            </div>
            <div className="order-1 lg:order-2 space-y-6">
              <div className="inline-block">
                <span className="px-4 py-2 bg-gradient-to-r from-accent-100 to-secondary-100 text-accent-700 rounded-full text-sm font-semibold">
                  💼 Conviértete en vendedor
                </span>
              </div>
              <h2 className="text-3xl md:text-5xl font-bold text-gray-900 leading-tight">
                Vende tus productos
                <span className="block text-gradient">y gana dinero</span>
              </h2>
              <p className="text-lg text-gray-600 leading-relaxed">
                Únete a nuestra comunidad de vendedores y alcanza miles de clientes. 
                Es gratis, rápido y sin complicaciones.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/sell-products">
                  <Button size="lg" className="btn-gradient shadow-lg hover:shadow-xl w-full sm:w-auto">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    Publicar Producto
                  </Button>
                </Link>
                <Link to="/products">
                  <Button size="lg" variant="outline" className="w-full sm:w-auto border-2 border-primary-600 text-primary-600 hover:bg-primary-50">
                    Ver Productos
                  </Button>
                </Link>
              </div>
              <div className="flex items-center space-x-6 pt-4 text-sm">
                <div className="flex items-center text-gray-600">
                  <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Registro gratis
                </div>
                <div className="flex items-center text-gray-600">
                  <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  Sin comisiones
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">¿Por qué NovaMarket?</h2>
          <p className="text-xl text-gray-600">La mejor experiencia de compra online</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card className="card-hover border-2 border-transparent hover:border-primary-200">
            <CardBody className="text-center py-10">
              <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
                <svg className="w-10 h-10 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                </svg>
              </div>
              <h3 className="font-bold text-xl mb-3 text-gray-900">Envío Gratis</h3>
              <p className="text-gray-600">En todos tus pedidos sin mínimo de compra. Recibe en 24-48 horas.</p>
            </CardBody>
          </Card>
          
          <Card className="card-hover border-2 border-transparent hover:border-secondary-200">
            <CardBody className="text-center py-10">
              <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-secondary-100 to-secondary-200 flex items-center justify-center">
                <svg className="w-10 h-10 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="font-bold text-xl mb-3 text-gray-900">Pago Seguro</h3>
              <p className="text-gray-600">Todas las transacciones son 100% seguras y protegidas.</p>
            </CardBody>
          </Card>
          
          <Card className="card-hover border-2 border-transparent hover:border-accent-200">
            <CardBody className="text-center py-10">
              <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-accent-100 to-accent-200 flex items-center justify-center">
                <svg className="w-10 h-10 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 className="font-bold text-xl mb-3 text-gray-900">Soporte 24/7</h3>
              <p className="text-gray-600">Estamos aquí para ayudarte en cualquier momento del día.</p>
            </CardBody>
          </Card>
        </div>
      </section>

      {/* Featured Products */}
      <section>
        <div className="flex justify-between items-center mb-10">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">Productos Destacados</h2>
            <p className="text-gray-600">Descubre nuestras mejores ofertas</p>
          </div>
          <Link to="/products" className="hidden md:block">
            <Button variant="outline" className="border-2 border-primary-600 text-primary-600 hover:bg-primary-50">
              Ver todos →
            </Button>
          </Link>
        </div>
        <ProductGrid products={featuredProducts} isLoading={isLoading} />
        <div className="text-center mt-8 md:hidden">
          <Link to="/products">
            <Button variant="outline" className="border-2 border-primary-600 text-primary-600 hover:bg-primary-50">
              Ver todos los productos
            </Button>
          </Link>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-600 via-secondary-600 to-accent-600 rounded-3xl"></div>
        <div className="relative rounded-3xl p-12 md:p-16 text-center text-white">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl md:text-5xl font-bold mb-6">
              ¿Listo para comenzar?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Únete a miles de clientes satisfechos y disfruta de la mejor experiencia de compra online.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/register">
                <Button size="lg" className="bg-white text-primary-600 hover:bg-gray-100 w-full sm:w-auto shadow-xl">
                  Crear Cuenta Gratis
                </Button>
              </Link>
              <Link to="/products">
                <Button size="lg" variant="outline" className="border-2 border-white text-white hover:bg-white/10 w-full sm:w-auto">
                  Explorar Productos
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
