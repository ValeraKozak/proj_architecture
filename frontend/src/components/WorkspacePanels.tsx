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
          <span className="eyebrow">Публікація</span>
          <h3>{user ? `Робоча зона ${user.full_name}` : "Попередній перегляд кабінету"}</h3>
        </div>
        <form className="stack-form" onSubmit={submitListing}>
          <label>
            Назва оголошення
            <input
              value={listingForm.title}
              onChange={(event) =>
                setListingForm((current) => ({ ...current, title: event.target.value }))
              }
            />
          </label>
          <label>
            Опис
            <textarea
              value={listingForm.description}
              onChange={(event) =>
                setListingForm((current) => ({ ...current, description: event.target.value }))
              }
            />
          </label>
          <div className="form-row">
            <label>
              Ціна
              <input
                type="number"
                value={listingForm.price}
                onChange={(event) =>
                  setListingForm((current) => ({ ...current, price: event.target.value }))
                }
              />
            </label>
            <label>
              Категорія
              <select
                value={listingForm.category_id}
                onChange={(event) =>
                  setListingForm((current) => ({ ...current, category_id: event.target.value }))
                }
              >
                <option value="">Оберіть категорію</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <label>
            Посилання на зображення
            <textarea
              value={listingForm.image_urls}
              placeholder="https://images.example.com/cover.jpg&#10;https://images.example.com/detail.jpg"
              onChange={(event) =>
                setListingForm((current) => ({ ...current, image_urls: event.target.value }))
              }
            />
          </label>
          <button className="cta-button" type="submit">
            Опублікувати оголошення
          </button>
        </form>
      </section>

      <section className="workspace-panel subtle">
        <div className="workspace-panel__header">
          <span className="eyebrow">Операційна панель</span>
          <h3>Модерація, категорії та повідомлення</h3>
        </div>
        <div className="mini-stats">
          <div>
            <strong>{pendingListings.length}</strong>
            <span>Чекають модерації</span>
          </div>
          <div>
            <strong>{messages.length}</strong>
            <span>Повідомлення</span>
          </div>
          <div>
            <strong>{myListings.length}</strong>
            <span>Мої оголошення</span>
          </div>
        </div>
        {user?.role === "admin" || user?.role === "moderator" ? (
          <form className="stack-form compact" onSubmit={submitCategory}>
            <label>
              Нова категорія
              <input
                value={categoryForm.name}
                onChange={(event) =>
                  setCategoryForm((current) => ({ ...current, name: event.target.value }))
                }
              />
            </label>
            <label>
              Опис категорії
              <input
                value={categoryForm.description}
                onChange={(event) =>
                  setCategoryForm((current) => ({ ...current, description: event.target.value }))
                }
              />
            </label>
            <button className="ghost-button" type="submit">
              Додати категорію
            </button>
          </form>
        ) : (
          <p className="helper-text">
            Увійдіть як `admin` або `moderator`, щоб керувати категоріями прямо з інтерфейсу.
          </p>
        )}
        <div className="workspace-list-preview">
          <div>
            <strong>Черга модерації</strong>
            <ul>
              {pendingListings.length ? (
                pendingListings.slice(0, 3).map((listing) => <li key={listing.id}>{listing.title}</li>)
              ) : (
                <li>Наразі немає оголошень у черзі.</li>
              )}
            </ul>
          </div>
          <div>
            <strong>Останні повідомлення</strong>
            <ul>
              {messages.length ? (
                messages.slice(0, 3).map((message) => <li key={message.id}>{message.body}</li>)
              ) : (
                <li>Поки що повідомлень немає.</li>
              )}
            </ul>
          </div>
        </div>
      </section>

      <section className="workspace-panel wide">
        <div className="workspace-panel__header">
          <span className="eyebrow">Асортимент</span>
          <h3>Ваші поточні оголошення</h3>
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
              <strong>Поки що немає жодного оголошення</strong>
              <p>Створіть першу публікацію у верхній формі, і вона одразу з’явиться тут.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
