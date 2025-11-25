// User Entity
export interface User {
  id_user: string;
  name: string;
  email: string;
  phone?: string;
  address?: string;
  created_at: string;
  last_updated: string;
}

export interface UserRegistration {
  name: string;
  email: string;
  password: string;
  phone?: string;
  address?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}
