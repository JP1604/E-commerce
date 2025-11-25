// Register Page - Modern Design
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@presentation/hooks/useAuth';
import { motion } from 'framer-motion';
import { 
  FaUser, 
  FaEnvelope, 
  FaLock, 
  FaPhone, 
  FaMapMarkerAlt,
  FaEye,
  FaEyeSlash,
  FaCheckCircle,
  FaExclamationTriangle
} from 'react-icons/fa';
import './RegisterPage.css';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { registerAsync, isRegistering, registerError } = useAuth();
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    address: '',
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [success, setSuccess] = useState(false);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'El nombre es requerido';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'El email es requerido';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    if (!formData.password) {
      newErrors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 6) {
      newErrors.password = 'La contraseña debe tener al menos 6 caracteres';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Las contraseñas no coinciden';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    try {
      await registerAsync({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        phone: formData.phone || undefined,
        address: formData.address || undefined,
      });
      
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <motion.div
          className="register-card"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="register-header">
            <h1>Crear Cuenta</h1>
            <p>Únete a nuestra comunidad</p>
          </div>

          {success && (
            <motion.div
              className="success-message"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <FaCheckCircle />
              <span>¡Cuenta creada exitosamente! Redirigiendo...</span>
            </motion.div>
          )}

          {registerError && (
            <motion.div
              className="error-message"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <FaExclamationTriangle />
              <span>{(registerError as any)?.response?.data?.detail || 'Error al registrar usuario'}</span>
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="register-form">
            {/* Name Field */}
            <div className="form-group">
              <label htmlFor="name">
                <FaUser /> Nombre Completo *
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className={errors.name ? 'error' : ''}
                placeholder="Juan Pérez"
                disabled={isRegistering}
              />
              {errors.name && <span className="error-text">{errors.name}</span>}
            </div>

            {/* Email Field */}
            <div className="form-group">
              <label htmlFor="email">
                <FaEnvelope /> Email *
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={errors.email ? 'error' : ''}
                placeholder="juan@ejemplo.com"
                disabled={isRegistering}
              />
              {errors.email && <span className="error-text">{errors.email}</span>}
            </div>

            {/* Password Field */}
            <div className="form-group">
              <label htmlFor="password">
                <FaLock /> Contraseña *
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
                  disabled={isRegistering}
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

            {/* Confirm Password Field */}
            <div className="form-group">
              <label htmlFor="confirmPassword">
                <FaLock /> Confirmar Contraseña *
              </label>
              <div className="password-input">
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className={errors.confirmPassword ? 'error' : ''}
                  placeholder="••••••••"
                  disabled={isRegistering}
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  tabIndex={-1}
                >
                  {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              {errors.confirmPassword && <span className="error-text">{errors.confirmPassword}</span>}
            </div>

            {/* Phone Field (Optional) */}
            <div className="form-group">
              <label htmlFor="phone">
                <FaPhone /> Teléfono
              </label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="+57 300 123 4567"
                disabled={isRegistering}
              />
            </div>

            {/* Address Field (Optional) */}
            <div className="form-group">
              <label htmlFor="address">
                <FaMapMarkerAlt /> Dirección
              </label>
              <input
                type="text"
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Calle 123 #45-67"
                disabled={isRegistering}
              />
            </div>

            <button 
              type="submit" 
              className="submit-button"
              disabled={isRegistering || success}
            >
              {isRegistering ? (
                <>
                  <span className="spinner"></span>
                  Registrando...
                </>
              ) : success ? (
                <>
                  <FaCheckCircle />
                  Registrado
                </>
              ) : (
                'Crear Cuenta'
              )}
            </button>
          </form>

          <div className="register-footer">
            <p>
              ¿Ya tienes cuenta?{' '}
              <a href="/login" onClick={(e) => { e.preventDefault(); navigate('/login'); }}>
                Iniciar Sesión
              </a>
            </p>
          </div>
        </motion.div>

        <div className="register-illustration">
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h2>Bienvenido a nuestra tienda</h2>
            <p>Regístrate para disfrutar de:</p>
            <ul>
              <li>✨ Ofertas exclusivas</li>
              <li>🚚 Envío gratis en tu primera compra</li>
              <li>🎁 Puntos de recompensa</li>
              <li>📦 Seguimiento de pedidos</li>
              <li>💳 Checkout rápido</li>
            </ul>
          </motion.div>
        </div>
      </div>
    </div>
  );
};
