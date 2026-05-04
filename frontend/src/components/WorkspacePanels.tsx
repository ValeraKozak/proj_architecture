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
  const canOperate = user?.role === "admin" || user?.role === "moderator";
  const [listingForm, setListingForm] = useState({
    title: "",
    description: "",
    price: "",
    category_id: "",
    image_urls: "",
  });
  const [categoryForm, setCategoryForm] = useState({ name: "", description: "" });
  const [listingBusy, setListingBusy] = useState(false);
  const [categoryBusy, setCategoryBusy] = useState(false);
  const [listingError, setListingError] = useState("");
  const [categoryError, setCategoryError] = useState("");
  const [listingSuccess, setListingSuccess] = useState("");
  const [categorySuccess, setCategorySuccess] = useState("");

  async function submitListing(event: FormEvent) {
    event.preventDefault();
    setListingError("");
    setListingSuccess("");

    if (!user) {
      setListingError("Увійдіть у систему, щоб створити оголошення.");
      return;
    }
    if (!listingForm.category_id) {
      setListingError("Оберіть категорію для оголошення.");
      return;
    }

    setListingBusy(true);

    try {
      await onCreateListing({
        title: listingForm.title.trim(),
        description: listingForm.description.trim(),
        price: Number(listingForm.price),
        category_id: Number(listingForm.category_id),
        image_urls: listingForm.image_urls
          .split("\n")
          .map((value) => value.trim())
          .filter(Boolean),
      });
      setListingForm({ title: "", description: "", price: "", category_id: "", image_urls: "" });
      setListingSuccess("Оголошення створено та відправлено на модерацію.");
    } catch (error) {
      setListingError(
        error instanceof Error ? error.message : "Не вдалося створити оголошення.",
      );
    } finally {
      setListingBusy(false);
    }
  }

  async function submitCategory(event: FormEvent) {
    event.preventDefault();
    setCategoryError("");
    setCategorySuccess("");

    if (!categoryForm.name.trim() || !categoryForm.description.trim()) {
      setCategoryError("Заповніть назву й опис категорії.");
      return;
    }

    setCategoryBusy(true);

    try {
      await onCreateCategory({
        name: categoryForm.name.trim(),
        description: categoryForm.description.trim(),
      });
      setCategoryForm({ name: "", description: "" });
      setCategorySuccess("Категорію успішно створено.");
    } catch (error) {
      setCategoryError(
        error instanceof Error ? error.message : "Не вдалося створити категорію.",
      );
    } finally {
      setCategoryBusy(false);
    }
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
                min="1"
                step="0.01"
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
              placeholder={
                "https://images.example.com/cover.jpg\nhttps://images.example.com/detail.jpg"
              }
              onChange={(event) =>
                setListingForm((current) => ({ ...current, image_urls: event.target.value }))
              }
            />
          </label>
          <button className="cta-button" disabled={listingBusy} type="submit">
            {listingBusy ? "Публікуємо..." : "Опублікувати оголошення"}
          </button>
          {listingError ? <p className="form-error">{listingError}</p> : null}
          {listingSuccess ? <p className="form-success">{listingSuccess}</p> : null}
        </form>
      </section>

      {canOperate ? (
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
            <button className="ghost-button" disabled={categoryBusy} type="submit">
              {categoryBusy ? "Створюємо..." : "Додати категорію"}
            </button>
            {categoryError ? <p className="form-error">{categoryError}</p> : null}
            {categorySuccess ? <p className="form-success">{categorySuccess}</p> : null}
          </form>
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
      ) : null}

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
              <p>Створіть першу публікацію у верхній формі, і вона одразу зʼявиться тут.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
