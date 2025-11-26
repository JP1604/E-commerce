import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useUserStore } from '../store/userStore';
import { orderRepository } from '../../infrastructure/repositories/OrderRepositoryImpl';
import { Card, CardBody, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const OrdersPage = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useUserStore();

  const { data: orders = [], isLoading, error } = useQuery({
    queryKey: ['orders', user?.id],
    queryFn: async () => {
      if (!user?.id) return [];
      const allOrders = await orderRepository.getAll();
      // Filtrar solo los pedidos del usuario actual
      return allOrders.filter(order => order.user_id === user.id);
    },
    enabled: isAuthenticated && !!user?.id,
  });

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  const getStatusBadge = (status) => {
    const statusStyles = {
      creada: 'bg-blue-100 text-blue-800',
      pagada: 'bg-green-100 text-green-800',
      enviada: 'bg-purple-100 text-purple-800',
      entregada: 'bg-gray-100 text-gray-800',
      cancelada: 'bg-red-100 text-red-800',
    };

    const statusText = {
      creada: 'Creada',
      pagada: 'Pagada',
      enviada: 'Enviada',
      entregada: 'Entregada',
      cancelada: 'Cancelada',
    };

    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusStyles[status] || 'bg-gray-100 text-gray-800'}`}>
        {statusText[status] || status}
      </span>
    );
  };

  if (!isAuthenticated) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardBody>
            <div className="text-center py-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Inicia sesión para ver tus pedidos</h2>
              <Button onClick={() => navigate('/login')}>Iniciar Sesión</Button>
            </div>
          </CardBody>
        </Card>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center items-center min-h-[400px]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardBody>
            <div className="text-center py-8">
              <h2 className="text-2xl font-bold text-red-600 mb-4">Error al cargar los pedidos</h2>
              <p className="text-gray-600">{error.message}</p>
            </div>
          </CardBody>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gradient mb-2">Mis Pedidos</h1>
          <p className="text-gray-600">Revisa el estado de tus compras</p>
        </div>

        {orders.length === 0 ? (
          <Card>
            <CardBody>
              <div className="text-center py-12">
                <svg className="w-24 h-24 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No tienes pedidos aún</h3>
                <p className="text-gray-600 mb-6">Comienza a explorar nuestros productos</p>
                <Button onClick={() => navigate('/products')}>Ver Productos</Button>
              </div>
            </CardBody>
          </Card>
        ) : (
          <div className="space-y-4">
            {orders.map((order) => (
              <Card key={order.id} className="hover:shadow-lg transition-shadow">
                <CardHeader className="border-b border-gray-100">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                    <div>
                      <p className="text-sm text-gray-500">Pedido #{order.id ? order.id.substring(0, 8) : 'N/A'}</p>
                      <p className="text-sm text-gray-600 mt-1">{formatDate(order.created_at)}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      {getStatusBadge(order.status)}
                      <p className="text-lg font-bold text-primary-600">{formatPrice(order.total)}</p>
                    </div>
                  </div>
                </CardHeader>
                
                <CardBody>
                  {/* Items del pedido */}
                  <div className="space-y-3 mb-4">
                    {order.items?.map((item) => (
                      <div key={item.id || Math.random()} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                        <div className="flex-1">
                          <p className="text-sm text-gray-600">
                            Producto ID: {item.product_id ? item.product_id.substring(0, 8) + '...' : 'N/A'}
                          </p>
                        </div>
                        <div className="flex items-center gap-4">
                          <span className="text-sm text-gray-600">Cantidad: {item.quantity}</span>
                          <span className="text-sm font-medium">{formatPrice(item.subtotal)}</span>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Acciones */}
                  <div className="flex flex-wrap gap-2 pt-3 border-t border-gray-100">
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => navigate(`/delivery/${order.id}`)}
                      disabled={!order.id}
                    >
                      Ver Detalles de Entrega
                    </Button>
                    
                    {order.status === 'creada' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          // Aquí podrías agregar lógica para pagar el pedido
                          alert('Funcionalidad de pago próximamente');
                        }}
                      >
                        Pagar Pedido
                      </Button>
                    )}
                  </div>
                </CardBody>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
