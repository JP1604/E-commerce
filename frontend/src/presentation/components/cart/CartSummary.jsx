import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardBody } from '../ui/Card';
import { Button } from '../ui/Button';

export const CartSummary = ({ total, itemCount, onCheckout, isLoading }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  return (
    <Card className="sticky top-24">
      <CardBody>
        <h3 className="text-xl font-bold mb-4">Resumen del Pedido</h3>
        <div className="space-y-3 mb-4">
          <div className="flex justify-between text-gray-600">
            <span>Productos ({itemCount})</span>
            <span>{formatPrice(total)}</span>
          </div>
          <div className="flex justify-between text-gray-600">
            <span>Envío</span>
            <span className="text-green-600">Gratis</span>
          </div>
          <hr className="my-2" />
          <div className="flex justify-between text-xl font-bold">
            <span>Total</span>
            <span className="text-blue-600">{formatPrice(total)}</span>
          </div>
        </div>
        <Button
          variant="primary"
          className="w-full mb-3"
          size="lg"
          onClick={onCheckout}
          isLoading={isLoading}
          disabled={itemCount === 0}
        >
          Proceder al Pago
        </Button>
        <Link to="/products">
          <Button variant="ghost" className="w-full">
            Seguir comprando
          </Button>
        </Link>
      </CardBody>
    </Card>
  );
};
