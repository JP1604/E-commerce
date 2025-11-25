import React from 'react';
import { Card, CardBody } from '../ui/Card';

export const CartItem = ({ item, product, onUpdateQuantity, onRemove }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  return (
    <Card>
      <CardBody className="flex items-center gap-4">
        <div className="h-20 w-20 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
          <span className="text-3xl">📦</span>
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-gray-800 truncate">
            {product?.name || `Producto #${item.product_id.slice(0, 8)}`}
          </h3>
          <p className="text-blue-600 font-bold">{formatPrice(item.unit_price)}</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => onUpdateQuantity(item.id, Math.max(1, item.quantity - 1))}
            className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition-colors"
          >
            -
          </button>
          <span className="w-8 text-center font-medium">{item.quantity}</span>
          <button
            onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
            className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition-colors"
          >
            +
          </button>
        </div>
        <div className="text-right">
          <p className="font-bold text-lg">{formatPrice(item.subtotal)}</p>
          <button
            onClick={() => onRemove(item.id)}
            className="text-red-500 hover:text-red-700 text-sm transition-colors"
          >
            Eliminar
          </button>
        </div>
      </CardBody>
    </Card>
  );
};
