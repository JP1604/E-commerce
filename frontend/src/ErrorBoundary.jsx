import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center p-8">
            <h1 className="text-4xl font-bold text-red-600 mb-4">Oops! Algo salió mal</h1>
            <p className="text-gray-600 mb-4">
              {this.state.error?.message || 'Ha ocurrido un error inesperado'}
            </p>
            <pre className="text-xs text-left bg-gray-100 p-4 rounded mb-4 max-w-2xl overflow-auto">
              {this.state.error?.stack || 'No hay detalles del error'}
            </pre>
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Recargar página
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
