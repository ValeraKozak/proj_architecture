import type { Category, Health, Listing, Message, User } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const api = {
  health: () => request<Health>("/health"),
  categories: () => request<Category[]>("/categories"),
  listings: () => request<Listing[]>("/listings"),
  login: (email: string, password: string) =>
    request<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  register: (email: string, full_name: string, password: string) =>
    request<User>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, full_name, password }),
    }),
  me: (token: string) =>
    request<User>("/users/me", {
      headers: { Authorization: `Bearer ${token}` },
    }),
  myListings: (token: string) =>
    request<Listing[]>("/listings/me/owned", {
      headers: { Authorization: `Bearer ${token}` },
    }),
  pendingListings: (token: string) =>
    request<Listing[]>("/listings/moderation/pending", {
      headers: { Authorization: `Bearer ${token}` },
    }),
  messages: (token: string) =>
    request<Message[]>("/messages/me", {
      headers: { Authorization: `Bearer ${token}` },
    }),
  createListing: (
    token: string,
    payload: { title: string; description: string; price: number; category_id: number },
  ) =>
    request<Listing>("/listings", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload),
    }),
  createCategory: (token: string, payload: { name: string; description: string }) =>
    request<Category>("/categories", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload),
    }),
};
