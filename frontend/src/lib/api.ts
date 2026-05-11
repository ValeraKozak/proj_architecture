import type {
  Category,
  Health,
  Listing,
  ListingFilters,
  Message,
  UploadBatch,
  User,
} from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export function resolveAssetUrl(url: string): string {
  if (!url) {
    return url;
  }
  if (url.startsWith("http://") || url.startsWith("https://") || url.startsWith("data:")) {
    return url;
  }
  if (!url.startsWith("/")) {
    return url;
  }
  if (API_BASE.startsWith("http://") || API_BASE.startsWith("https://")) {
    return `${new URL(API_BASE).origin}${url}`;
  }
  return url;
}

export class APIError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail || `Request failed: ${status}`);
    this.name = "APIError";
    this.status = status;
    this.detail = detail || `Request failed: ${status}`;
  }
}

function formatValidationDetail(detail: unknown): string {
  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (!item || typeof item !== "object") {
          return "Validation error";
        }

        const issue = item as {
          loc?: Array<string | number>;
          msg?: string;
        };
        const path = issue.loc?.slice(1).join(".") ?? "field";
        return `${path}: ${issue.msg ?? "Invalid value"}`;
      })
      .join("; ");
  }

  if (detail && typeof detail === "object" && "detail" in detail) {
    return formatValidationDetail((detail as { detail?: unknown }).detail);
  }

  return "";
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers ?? {});
  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const contentType = response.headers.get("content-type") ?? "";
    let detail = "";

    if (contentType.includes("application/json")) {
      const payload = (await response.json()) as { detail?: unknown };
      detail = formatValidationDetail(payload.detail);
    } else {
      detail = await response.text();
    }

    throw new APIError(response.status, detail || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

async function requestFormData<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers ?? {});
  headers.delete("Content-Type");

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const contentType = response.headers.get("content-type") ?? "";
    let detail = "";

    if (contentType.includes("application/json")) {
      const payload = (await response.json()) as { detail?: unknown };
      detail = formatValidationDetail(payload.detail);
    } else {
      detail = await response.text();
    }

    throw new APIError(response.status, detail || `Request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}

function withQuery(path: string, params: Record<string, string | number | undefined>) {
  const searchParams = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") {
      searchParams.set(key, String(value));
    }
  }
  const query = searchParams.toString();
  return query ? `${path}?${query}` : path;
}

export const api = {
  health: () => request<Health>("/health"),
  categories: () => request<Category[]>("/categories"),
  listings: (filters: ListingFilters = {}) =>
    request<Listing[]>(
      withQuery("/listings", {
        query: filters.query,
        category_id: filters.category_id,
        min_price: filters.min_price,
        max_price: filters.max_price,
        sort_by: filters.sort_by,
        sort_order: filters.sort_order,
      }),
    ),
  listingById: (listingId: number, token?: string) =>
    request<Listing>(`/listings/${listingId}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }),
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
  sendMessage: (
    token: string,
    payload: {
      listing_id: number;
      recipient_id: number;
      body: string;
    },
  ) =>
    request<Message>("/messages", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload),
    }),
  createListing: (
    token: string,
    payload: {
      title: string;
      description: string;
      price: number;
      category_id: number;
      image_urls: string[];
    },
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
  uploadImages: async (token: string, files: File[]) => {
    const formData = new FormData();
    for (const file of files) {
      formData.append("files", file);
    }
    const result = await requestFormData<UploadBatch>("/uploads/images", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    });
    return result.files.map((file) => file.url);
  },
  moderateListing: (
    token: string,
    listing_id: number,
    payload: { approved: boolean; rejection_reason?: string | null },
  ) =>
    request<Listing>(`/moderation/listings/${listing_id}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload),
    }),
};
