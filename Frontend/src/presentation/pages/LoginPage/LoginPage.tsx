// Login Page - Modern Design
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@presentation/hooks/useAuth';
import { motion } from 'framer-motion';
import { 
  FaEnvelope, 
  FaLock, 
  FaEye,
  FaEyeSlash,
  FaCheckCircle,
  FaExclamationTriangle
} from 'react-icons/fa';
import './LoginPage.css';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { loginAsync, isLoggingIn, loginError } = useAuth();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [success, setSuccess] = useState(false);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.email.trim()) {
      newErrors.email = 'El email es requerido';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    if (!formData.password) {
      newErrors.password = 'La contraseña es requerida';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    try {
      const result = await loginAsync({
        email: formData.email,
        password: formData.password,
      });
      
      setSuccess(true);
      // Store user ID in localStorage (temporary solution)
      localStorage.setItem('userId', result.user_id);
      
      setTimeout(() => {
        navigate('/');
      }, 1500);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <motion.div
          className="login-card"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="login-header">
            <h1>Bienvenido de Nuevo</h1>
            <p>Inicia sesión para continuar</p>
          </div>

          {success && (
            <motion.div
              className="success-message"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <FaCheckCircle />
              <span>¡Inicio de sesión exitoso! Redirigiendo...</span>
            </motion.div>
          )}

          {loginError && (
            <motion.div
              className="error-message"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <FaExclamationTriangle />
              <span>{(loginError as any)?.response?.data?.detail || 'Credenciales inválidas'}</span>
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="email">
                <FaEnvelope /> Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={errors.email ? 'error' : ''}
                placeholder="tu@email.com"
                disabled={isLoggingIn}
              />
              {errors.email && <span className="error-text">{errors.email}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="password">
                <FaLock /> Contraseña
              </label>
              <div className="password-input">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className={errors.password ? 'error' : ''}
                  placeholder="••••••••"
                  disabled={isLoggingIn}
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setShowPassword(!showPassword)}
                  tabIndex={-1}
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              {errors.password && <span className="error-text">{errors.password}</span>}
            </div>

            <button 
              type="submit" 
              className="submit-button"
              disabled={isLoggingIn || success}
            >
              {isLoggingIn ? (
                <>
                  <span className="spinner"></span>
                  Iniciando sesión...
                </>
              ) : success ? (
                <>
                  <FaCheckCircle />
                  Éxito
                </>
              ) : (
                'Iniciar Sesión'
              )}
            </button>
          </form>

          <div className="login-footer">
            <p>
              ¿No tienes cuenta?{' '}
              <a href="/register" onClick={(e) => { e.preventDefault(); navigate('/register'); }}>
                Regístrate aquí
              </a>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};
