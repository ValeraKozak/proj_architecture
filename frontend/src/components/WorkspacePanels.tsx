import { FormEvent, useState } from "react";

import type { Category, Listing, Message, User } from "../lib/types";
import { ListingCard } from "./ListingCard";

interface WorkspacePanelsProps {
  user: User | null;
  categories: Category[];
  myListings: Listing[];
  pendingListings: Listing[];
  messages: Message[];
  onCreateListing: (payload: {
    title: string;
    description: string;
    price: number;
    category_id: number;
    image_urls: string[];
  }) => Promise<void>;
  onCreateCategory: (payload: { name: string; description: string }) => Promise<void>;
}

export function WorkspacePanels({
  user,
  categories,
  myListings,
  pendingListings,
  messages,
  onCreateListing,
  onCreateCategory,
}: WorkspacePanelsProps) {
  const [listingForm, setListingForm] = useState({
    title: "",
    description: "",
    price: "",
    category_id: "",
    image_urls: "",
  });
  const [categoryForm, setCategoryForm] = useState({ name: "", description: "" });

  async function submitListing(event: FormEvent) {
    event.preventDefault();
    await onCreateListing({
      title: listingForm.title,
      description: listingForm.description,
      price: Number(listingForm.price),
      category_id: Number(listingForm.category_id),
      image_urls: listingForm.image_urls
        .split("\n")
        .map((value) => value.trim())
        .filter(Boolean),
    });
    setListingForm({ title: "", description: "", price: "", category_id: "", image_urls: "" });
  }

  async function submitCategory(event: FormEvent) {
    event.preventDefault();
    await onCreateCategory(categoryForm);
    setCategoryForm({ name: "", description: "" });
  }

  return (
    <div className="workspace-grid">
      <section className="workspace-panel">
        <div className="workspace-panel__header">
          <span className="eyebrow">Control room</span>
          <h3>{user ? `${user.full_name}'s workspace` : "Workspace preview"}</h3>
        </div>
        <form className="stack-form" onSubmit={submitListing}>
          <label>
            Title
            <input
              value={listingForm.title}
              onChange={(event) => setListingForm((current) => ({ ...current, title: event.target.value }))}
            />
          </label>
          <label>
            Description
            <textarea
              value={listingForm.description}
              onChange={(event) =>
                setListingForm((current) => ({ ...current, description: event.target.value }))
              }
            />
          </label>
          <div className="form-row">
            <label>
              Price
              <input
                type="number"
                value={listingForm.price}
                onChange={(event) => setListingForm((current) => ({ ...current, price: event.target.value }))}
              />
            </label>
            <label>
              Category
              <select
                value={listingForm.category_id}
                onChange={(event) =>
                  setListingForm((current) => ({ ...current, category_id: event.target.value }))
                }
              >
                <option value="">Select</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <label>
            Image URLs
            <textarea
              value={listingForm.image_urls}
              placeholder="https://images.example.com/cover.jpg&#10;https://images.example.com/detail.jpg"
              onChange={(event) =>
                setListingForm((current) => ({ ...current, image_urls: event.target.value }))
              }
            />
          </label>
          <button className="cta-button" type="submit">
            Publish listing
          </button>
        </form>
      </section>

      <section className="workspace-panel subtle">
        <div className="workspace-panel__header">
          <span className="eyebrow">Moderation</span>
          <h3>Queue and messaging snapshot</h3>
        </div>
        <div className="mini-stats">
          <div>
            <strong>{pendingListings.length}</strong>
            <span>Pending listings</span>
          </div>
          <div>
            <strong>{messages.length}</strong>
            <span>Messages</span>
          </div>
          <div>
            <strong>{myListings.length}</strong>
            <span>Owned listings</span>
          </div>
        </div>
        {user?.role === "admin" || user?.role === "moderator" ? (
          <form className="stack-form compact" onSubmit={submitCategory}>
            <label>
              New category
              <input
                value={categoryForm.name}
                onChange={(event) =>
                  setCategoryForm((current) => ({ ...current, name: event.target.value }))
                }
              />
            </label>
            <label>
              Description
              <input
                value={categoryForm.description}
                onChange={(event) =>
                  setCategoryForm((current) => ({ ...current, description: event.target.value }))
                }
              />
            </label>
            <button className="ghost-button" type="submit">
              Add category
            </button>
          </form>
        ) : (
          <p className="helper-text">
            Sign in as `admin` or `moderator` to manage categories directly from the frontend.
          </p>
        )}
      </section>

      <section className="workspace-panel wide">
        <div className="workspace-panel__header">
          <span className="eyebrow">Owned listings</span>
          <h3>Your current inventory</h3>
        </div>
        <div className="listing-grid compact">
          {myListings.length ? (
            myListings.map((listing) => (
              <ListingCard
                key={listing.id}
                listing={listing}
                category={categories.find((category) => category.id === listing.category_id)}
              />
            ))
          ) : (
            <div className="empty-card">
              <strong>No listings yet</strong>
              <p>Create your first post from the control panel to fill this grid.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
