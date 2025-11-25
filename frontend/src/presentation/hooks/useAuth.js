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
      setUser(user);
      queryClient.invalidateQueries({ queryKey: ['cart'] });
      navigate('/');
    },
    onError: (error) => {
      console.error('Login error:', error);
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
