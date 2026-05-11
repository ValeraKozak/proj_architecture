export type Role = "user" | "moderator" | "admin";
export type ListingStatus = "draft" | "pending" | "approved" | "rejected" | "archived";

export interface Category {
  id: number;
  name: string;
  description: string;
}

export interface Listing {
  id: number;
  title: string;
  description: string;
  price: number;
  status: ListingStatus;
  rejection_reason?: string | null;
  owner_id: number;
  owner_name?: string | null;
  category_id: number;
  created_at?: string | null;
  image_urls: string[];
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: Role;
  is_blocked: boolean;
}

export interface Message {
  id: number;
  listing_id: number;
  sender_id: number;
  sender_name?: string | null;
  recipient_id: number;
  recipient_name?: string | null;
  body: string;
  created_at?: string | null;
}

export interface UploadBatch {
  files: Array<{ url: string }>;
}

export interface Health {
  status: string;
  environment: string;
}

export interface ListingFilters {
  query?: string;
  category_id?: number;
  min_price?: number;
  max_price?: number;
  sort_by?: "created_at" | "price";
  sort_order?: "asc" | "desc";
}
