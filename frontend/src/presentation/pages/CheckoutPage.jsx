import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';
import { useUserStore } from '../store/userStore';
import { useCreateOrder } from '../hooks/useOrder';
import { Button } from '../components/ui/Button';
import { Card, CardBody, CardHeader } from '../components/ui/Card';

export const CheckoutPage = () => {
  const navigate = useNavigate();
  const { cart, items, getTotal } = useCartStore();
  const { user, isAuthenticated } = useUserStore();
  const createOrder = useCreateOrder();
  const [paymentMethod, setPaymentMethod] = useState('credit_card');
  
  // Delivery date and time states
  const [deliveryDate, setDeliveryDate] = useState('');
  const [deliveryTimeStart, setDeliveryTimeStart] = useState('09:00');
  const [deliveryTimeEnd, setDeliveryTimeEnd] = useState('17:00');
  
  // Set minimum date to tomorrow
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const minDate = tomorrow.toISOString().split('T')[0];
  
  // Initialize delivery date to tomorrow
  useEffect(() => {
    if (!deliveryDate) {
      setDeliveryDate(minDate);
    }
  }, [minDate, deliveryDate]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const handleCreateOrder = async () => {
    if (!isAuthenticated || !user?.id) {
      alert('Debes iniciar sesión para realizar la compra');
      navigate('/login');
      return;
    }

    if (!cart?.id || items.length === 0) {
      alert('El carrito está vacío');
      navigate('/cart');
      return;
    }

    try {
      console.log('🛒 Creando orden con items:', items);
      console.log('📅 Delivery date:', deliveryDate);
      console.log('⏰ Delivery time:', deliveryTimeStart, '-', deliveryTimeEnd);
      
      const order = await createOrder.mutateAsync({
        items,
        paymentMethod,
        deliveryDate,
        deliveryTimeStart,
        deliveryTimeEnd,
      });

      console.log('✅ Orden creada:', order);
      console.log('🆔 Order ID para delivery:', order.id);
      alert(`✅ Orden creada exitosamente!`);
      
      // Redirigir a la página de delivery con el ID de la orden
      navigate(`/delivery/${order.id || order.id_order}`);
    } catch (error) {
      console.error('❌ Error creando orden:', error);
      alert(`❌ Error: ${error.response?.data?.detail || error.message || 'No se pudo crear la orden'}`);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardBody>
            <h2 className="text-2xl font-bold mb-4">Debes iniciar sesión</h2>
            <p className="mb-4">Para realizar una compra, primero debes iniciar sesión.</p>
            <Button onClick={() => navigate('/login')}>Iniciar sesión</Button>
          </CardBody>
        </Card>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardBody>
            <h2 className="text-2xl font-bold mb-4">Carrito vacío</h2>
            <p className="mb-4">No hay productos en tu carrito.</p>
            <Button onClick={() => navigate('/products')}>Ver productos</Button>
          </CardBody>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Finalizar Compra</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Resumen de productos */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <h2 className="text-xl font-bold">Productos ({items.length})</h2>
            </CardHeader>
            <CardBody>
              <div className="space-y-4">
                {items.map((item) => (
                  <div key={item.id} className="flex items-center justify-between border-b pb-4">
                    <div className="flex-1">
                      <h3 className="font-semibold">Producto ID: {item.product_id}</h3>
                      <p className="text-sm text-gray-600">
                        Cantidad: {item.quantity} x {formatPrice(item.unit_price)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-lg">{formatPrice(item.subtotal)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>

          {/* Método de pago */}
          <Card className="mt-6">
            <CardHeader>
              <h2 className="text-xl font-bold">Método de Pago</h2>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                <label className="flex items-center space-x-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="credit_card"
                    checked={paymentMethod === 'credit_card'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="w-4 h-4"
                  />
                  <div>
                    <p className="font-semibold">💳 Tarjeta de Crédito</p>
                    <p className="text-sm text-gray-600">Pago seguro con tarjeta</p>
                  </div>
                </label>

                <label className="flex items-center space-x-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="debit_card"
                    checked={paymentMethod === 'debit_card'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="w-4 h-4"
                  />
                  <div>
                    <p className="font-semibold">💰 Tarjeta de Débito</p>
                    <p className="text-sm text-gray-600">Débito inmediato</p>
                  </div>
                </label>

                <label className="flex items-center space-x-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="paypal"
                    checked={paymentMethod === 'paypal'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="w-4 h-4"
                  />
                  <div>
                    <p className="font-semibold">🅿️ PayPal</p>
                    <p className="text-sm text-gray-600">Pago con PayPal</p>
                  </div>
                </label>
              </div>
            </CardBody>
          </Card>

          {/* Fecha y hora de entrega */}
          <Card className="mt-6">
            <CardHeader>
              <h2 className="text-xl font-bold">📅 Fecha de Entrega</h2>
            </CardHeader>
            <CardBody>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Fecha de entrega
                  </label>
                  <input
                    type="date"
                    value={deliveryDate}
                    onChange={(e) => setDeliveryDate(e.target.value)}
                    min={minDate}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-1">Selecciona el día que deseas recibir tu pedido</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Hora inicio
                    </label>
                    <input
                      type="time"
                      value={deliveryTimeStart}
                      onChange={(e) => setDeliveryTimeStart(e.target.value)}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Hora fin
                    </label>
                    <input
                      type="time"
                      value={deliveryTimeEnd}
                      onChange={(e) => setDeliveryTimeEnd(e.target.value)}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      required
                    />
                  </div>
                </div>
                <p className="text-xs text-gray-500">Ventana de entrega disponible</p>
              </div>
            </CardBody>
          </Card>
        </div>

        {/* Resumen de orden */}
        <div>
          <Card className="sticky top-4">
            <CardHeader>
              <h2 className="text-xl font-bold">Resumen de la Orden</h2>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Subtotal</span>
                  <span className="font-semibold">{formatPrice(getTotal())}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Envío</span>
                  <span className="font-semibold text-green-600">Gratis</span>
                </div>
                <div className="border-t pt-3 mt-3">
                  <div className="flex justify-between text-lg">
                    <span className="font-bold">Total</span>
                    <span className="font-bold text-primary-600">{formatPrice(getTotal())}</span>
                  </div>
                </div>
              </div>

              <div className="mt-6 space-y-3">
                <Button
                  variant="primary"
                  className="w-full"
                  onClick={handleCreateOrder}
                  disabled={createOrder.isPending}
                  isLoading={createOrder.isPending}
                >
                  {createOrder.isPending ? 'Procesando...' : '🛒 Realizar Pedido'}
                </Button>

                <Button
                  variant="secondary"
                  className="w-full"
                  onClick={() => navigate('/cart')}
                >
                  Volver al Carrito
                </Button>
              </div>

              <div className="mt-4 p-3 bg-blue-50 rounded-lg text-sm text-gray-700">
                <p className="flex items-center">
                  <span className="mr-2">🔒</span>
                  Pago 100% seguro y protegido
                </p>
              </div>
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
};
