import type { LoginResponse, User } from '@/interfaces'
import { useAuthStore } from '@/stores/auth'

const API_BASE_URL = 'http://localhost:8000'

// Helper que siempre aÃ±ade el Authorization si hay token
export async function apiFetch(path: string, config: RequestInit = {}) {
  const auth = useAuthStore()

  // Partimos de los headers que ya vengan en config
  const headers = new Headers(config.headers || {})

  if (auth.token) {
    headers.set('Authorization', `Bearer ${auth.token}`)
  }

  config.headers = headers

  return await fetch(`${API_BASE_URL}${path}`, config)
}

export async function login(
  username: string,
  password: string,
): Promise<LoginResponse | undefined> {
  const body = new URLSearchParams({
    username,
    password,
  })

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  })

  if (response.ok) {
    return await response.json()
  }
}

export async function fetchUsers(): Promise<User[]> {
  const response = await apiFetch('/users', {})
  return await response.json()
}

export async function fetchUser(id: number): Promise<User | null> {
  const response = await apiFetch(`/users/${id}`, {})
  return await response.json()
}

export async function patchUser(id: number, userData: User) {
  const response = await apiFetch(`/users/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  })
  return await response.json()
}

// Crear usuario
export async function createUser(userData: {
  username: string
  fullname: string
  password: string
}) {
  const response = await apiFetch('/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  })

  if (!response.ok) {
    throw new Error(`Error creating user: ${response.status}`)
  }

  return await response.json()
}