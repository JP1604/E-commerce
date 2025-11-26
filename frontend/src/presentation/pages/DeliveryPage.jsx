import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { deliveryRepository } from '../../infrastructure/repositories';
import { Card, CardBody, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';

export const DeliveryPage = () => {
  const { orderId } = useParams();
  const navigate = useNavigate();
  const [delivery, setDelivery] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDelivery();
  }, [orderId]);

  const loadDelivery = async () => {
    try {
      setLoading(true);
      const deliveryData = await deliveryRepository.getByOrderId(orderId);
      setDelivery(deliveryData);
    } catch (err) {
      console.error('Error loading delivery:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      'booked': { variant: 'info', label: '📅 Reservado' },
      'in_transit': { variant: 'warning', label: '🚚 En tránsito' },
      'delivered': { variant: 'success', label: '✅ Entregado' },
      'cancelled': { variant: 'danger', label: '❌ Cancelado' },
    };
    
    const config = statusMap[status] || { variant: 'secondary', label: status };
    return <Badge variant={config.variant}>{config.label}</Badge>;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-16">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando información de entrega...</p>
        </div>
      </div>
    );
  }

  if (error && !delivery) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <h2 className="text-2xl font-bold">⚠️ Información de Entrega no Disponible</h2>
          </CardHeader>
          <CardBody>
            <p className="text-gray-600 mb-6">
              La información de entrega para esta orden aún no está disponible. 
              El delivery se crea automáticamente al realizar el pedido. 
              Por favor, intenta recargar la página en unos momentos.
            </p>
            <div className="space-y-3">
              <Button
                variant="primary"
                onClick={loadDelivery}
                className="w-full"
              >
                🔄 Recargar
              </Button>
              <Button
                variant="secondary"
                onClick={() => navigate('/products')}
                className="w-full"
              >
                Volver a Productos
              </Button>
            </div>
          </CardBody>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Button variant="secondary" onClick={() => navigate('/products')}>
          ← Volver a Productos
        </Button>
      </div>

      <h1 className="text-3xl font-bold mb-8">🚚 Información de Entrega</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Información principal del delivery */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold">Detalles del Delivery</h2>
                {delivery?.status && getStatusBadge(delivery.status)}
              </div>
            </CardHeader>
            <CardBody>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">ID de Delivery</p>
                    <p className="font-mono text-sm">{delivery?.id_delivery || delivery?.id}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">ID de Orden</p>
                    <p className="font-mono text-sm">{delivery?.order_id || delivery?.id_order}</p>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <h3 className="font-semibold mb-3">📅 Programación de Entrega</h3>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                      <span className="text-sm text-gray-700">Fecha programada:</span>
                      <span className="font-semibold">{delivery?.delivery_booked_schedule}</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                      <span className="text-sm text-gray-700">Inicio de ventana:</span>
                      <span className="font-semibold">{formatDate(delivery?.booking_start)}</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                      <span className="text-sm text-gray-700">Fin de ventana:</span>
                      <span className="font-semibold">{formatDate(delivery?.booking_end)}</span>
                    </div>
                  </div>
                </div>

                {delivery?.created_at && (
                  <div className="border-t pt-4">
                    <p className="text-sm text-gray-600">Creado el:</p>
                    <p className="font-semibold">{formatDate(delivery.created_at)}</p>
                  </div>
                )}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* Timeline de estados */}
        <div>
          <Card>
            <CardHeader>
              <h2 className="text-xl font-bold">Estado del Pedido</h2>
            </CardHeader>
            <CardBody>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white">
                    ✓
                  </div>
                  <div>
                    <p className="font-semibold">Pedido Confirmado</p>
                    <p className="text-sm text-gray-600">Tu pedido ha sido procesado</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white ${
                    delivery?.status === 'booked' || delivery?.status === 'in_transit' || delivery?.status === 'delivered' 
                      ? 'bg-green-500' 
                      : 'bg-gray-300'
                  }`}>
                    {delivery?.status === 'booked' || delivery?.status === 'in_transit' || delivery?.status === 'delivered' ? '✓' : '○'}
                  </div>
                  <div>
                    <p className="font-semibold">Delivery Reservado</p>
                    <p className="text-sm text-gray-600">Fecha de entrega programada</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white ${
                    delivery?.status === 'in_transit' || delivery?.status === 'delivered' 
                      ? 'bg-green-500' 
                      : 'bg-gray-300'
                  }`}>
                    {delivery?.status === 'in_transit' || delivery?.status === 'delivered' ? '✓' : '○'}
                  </div>
                  <div>
                    <p className="font-semibold">En Camino</p>
                    <p className="text-sm text-gray-600">Tu pedido está siendo transportado</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white ${
                    delivery?.status === 'delivered' 
                      ? 'bg-green-500' 
                      : 'bg-gray-300'
                  }`}>
                    {delivery?.status === 'delivered' ? '✓' : '○'}
                  </div>
                  <div>
                    <p className="font-semibold">Entregado</p>
                    <p className="text-sm text-gray-600">Pedido recibido con éxito</p>
                  </div>
                </div>
              </div>

              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-700">
                  <strong>📍 Nota:</strong> Recibirás una notificación cuando tu pedido esté en camino.
                </p>
              </div>
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
};
