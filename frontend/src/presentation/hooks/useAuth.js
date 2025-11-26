import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userRepository } from '../../infrastructure/repositories';
import { useUserStore } from '../store/userStore';
import { useNavigate } from 'react-router-dom';

export const useLogin = () => {
  const { setUser } = useUserStore();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (credentials) => userRepository.login(credentials),
    onSuccess: (user) => {
      console.log('✅ Login exitoso, datos recibidos:', user);
      setUser(user);
      console.log('✅ Usuario guardado en store');
      queryClient.invalidateQueries({ queryKey: ['cart'] });
      navigate('/');
    },
    onError: (error) => {
      console.error('❌ Login error:', error);
      console.error('❌ Error response:', error.response?.data);
    },
  });
};

export const useRegister = () => {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: (userData) => userRepository.create(userData),
    onSuccess: () => {
      navigate('/login');
    },
    onError: (error) => {
      console.error('Register error:', error);
    },
  });
};

export const useLogout = () => {
  const { logout } = useUserStore();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return () => {
    logout();
    queryClient.clear();
    navigate('/login');
  };
};
