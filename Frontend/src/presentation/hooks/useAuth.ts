// Auth Hook
import { useMutation } from '@tanstack/react-query';
import { container } from '@infrastructure/di/container';
import { UserRegistration, UserLogin } from '@domain/entities/User';

export const useAuth = () => {
  const registerMutation = useMutation({
    mutationFn: async (data: UserRegistration) => {
      const useCase = container.registerUserUseCase;
      return await useCase.execute(data);
    },
  });

  const loginMutation = useMutation({
    mutationFn: async (data: UserLogin) => {
      const useCase = container.loginUserUseCase;
      return await useCase.execute(data);
    },
  });

  return {
    register: registerMutation.mutate,
    registerAsync: registerMutation.mutateAsync,
    login: loginMutation.mutate,
    loginAsync: loginMutation.mutateAsync,
    isRegistering: registerMutation.isPending,
    isLoggingIn: loginMutation.isPending,
    registerError: registerMutation.error,
    loginError: loginMutation.error,
  };
};
