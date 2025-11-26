import React, { useState, useEffect } from 'react';
import { useProduct } from '../../hooks/useProducts';
import { Card, CardBody } from '../ui/Card';

export const CartItem = ({ item, product, onUpdateQuantity, onRemove, isUpdating, isRemoving }) => {
  const { data: productData } = useProduct(item.product_id);
  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const [localQuantity, setLocalQuantity] = useState(item.quantity);

  useEffect(() => {
    if (item.quantity !== localQuantity) {
      setLocalQuantity(item.quantity);
    }
  }, [item.quantity]);

  // Debounce updates so we don't send a request on every keystroke
  useEffect(() => {
    const handler = setTimeout(() => {
      if (localQuantity !== item.quantity) {
        onUpdateQuantity(item.id, Math.max(1, Number(localQuantity)));
      }
    }, 400);
    return () => clearTimeout(handler);
  }, [localQuantity, item.quantity, item.id, onUpdateQuantity]);

  return (
    <Card>
      <CardBody className="flex items-center gap-4">
        <div className="h-20 w-20 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
          <span className="text-3xl">📦</span>
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-gray-800 truncate">
            {productData?.name || product?.name || `Producto #${item.product_id.slice(0, 8)}`}
          </h3>
          <p className="text-blue-600 font-bold">{formatPrice(item.unit_price)}</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              console.log('[CartItem] Minus click for item', item.id, 'localQuantity:', localQuantity, 'itemQuantity:', item.quantity);
              const newQ = Math.max(1, Number(localQuantity) - 1);
              setLocalQuantity(newQ);
              // Debounced effect will handle the actual update
            }}
            className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition-colors"
            disabled={isUpdating || isRemoving || item.quantity <= 1}
          >
            -
          </button>
          <input
            type="number"
            min="1"
            value={localQuantity}
            onChange={(e) => setLocalQuantity(Math.max(1, parseInt(e.target.value || '1')))}
            onBlur={() => onUpdateQuantity(item.id, Math.max(1, Number(localQuantity)))}
            className="w-16 text-center font-medium border-2 border-gray-200 rounded-md py-1"
            disabled={isUpdating || isRemoving}
          />
          <button
            onClick={() => {
              console.log('[CartItem] Plus click for item', item.id, 'localQuantity:', localQuantity, 'itemQuantity:', item.quantity);
              const newQ = Number(localQuantity) + 1;
              setLocalQuantity(newQ);
              // Debounced effect will handle the actual update
            }}
            className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition-colors"
            disabled={isUpdating || isRemoving}
          >
            +
          </button>
        </div>
        <div className="text-right">
          <p className="font-bold text-lg">{formatPrice(item.subtotal)}</p>
          <button
            onClick={() => {
              console.log('[CartItem] Remove clicked for item', item.id);
              onRemove(item.id);
            }}
            className="text-red-500 hover:text-red-700 text-sm transition-colors"
            disabled={isRemoving || isUpdating}
          >
            {isRemoving ? 'Eliminando...' : 'Eliminar'}
          </button>
        </div>
      </CardBody>
    </Card>
  );
};
