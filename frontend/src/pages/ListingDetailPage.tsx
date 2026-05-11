import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { ConversationPanel } from "../components/ConversationPanel";
import { SectionTitle } from "../components/SectionTitle";
import { APIError, api, resolveAssetUrl } from "../lib/api";
import type { Category, Listing, Message, User } from "../lib/types";

interface ListingDetailPageProps {
  token: string;
  user: User | null;
  categories: Category[];
  listings: Listing[];
  messages: Message[];
  onSendMessage: (payload: { listing_id: number; recipient_id: number; body: string }) => Promise<void>;
}

export function ListingDetailPage({
  token,
  user,
  categories,
  listings,
  messages,
  onSendMessage,
}: ListingDetailPageProps) {
  const params = useParams();
  const listingId = Number(params.listingId);
  const [listing, setListing] = useState<Listing | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeImageIndex, setActiveImageIndex] = useState(0);

  useEffect(() => {
    if (!Number.isFinite(listingId)) {
      setError("Некоректний ідентифікатор оголошення.");
      setLoading(false);
      return;
    }

    setLoading(true);
    setError("");

    api
      .listingById(listingId, token || undefined)
      .then((result) => {
        setListing(result);
        setActiveImageIndex(0);
      })
      .catch((loadError) => {
        if (loadError instanceof APIError && loadError.status === 404) {
          setError("Оголошення не знайдено або воно ще не доступне для публічного перегляду.");
          return;
        }
        setError(loadError instanceof Error ? loadError.message : "Не вдалося завантажити оголошення.");
      })
      .finally(() => setLoading(false));
  }, [listingId, token]);

  const category = useMemo(
    () => categories.find((entry) => entry.id === listing?.category_id),
    [categories, listing?.category_id],
  );
  const relatedListings = useMemo(() => {
    if (!listing) {
      return [];
    }
    return listings
      .filter((candidate) => candidate.id !== listing.id && candidate.category_id === listing.category_id)
      .slice(0, 3);
  }, [listing, listings]);
  const conversationMessages = useMemo(() => {
    if (!listing || !user) {
      return [];
    }
    return messages.filter((message) => {
      const sameListing = message.listing_id === listing.id;
      const withOwner =
        message.sender_id === listing.owner_id || message.recipient_id === listing.owner_id;
      const withUser = message.sender_id === user.id || message.recipient_id === user.id;
      return sameListing && withOwner && withUser;
    });
  }, [listing, messages, user]);
  const canMessageSeller = Boolean(user && listing && user.id !== listing.owner_id);
  const galleryImages = listing?.image_urls ?? [];
  const activeImage = galleryImages[activeImageIndex];

  if (loading) {
    return (
      <div className="page-shell">
        <section className="content-block">
          <div className="empty-card">
            <strong>Завантажуємо оголошення</strong>
            <p>Збираємо фото, опис, продавця і пов’язаний діалог.</p>
          </div>
        </section>
      </div>
    );
  }

  if (!listing) {
    return (
      <div className="page-shell">
        <section className="content-block">
          <div className="empty-card">
            <strong>Не вдалося відкрити оголошення</strong>
            <p>{error || "Спробуйте повернутися до каталогу та відкрити іншу пропозицію."}</p>
            <Link className="ghost-button" to="/catalog">
              Повернутися в каталог
            </Link>
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="page-shell">
      <section className="content-block listing-detail-shell">
        <div className="listing-detail-gallery">
          <div className="listing-detail-gallery__hero">
            {activeImage ? (
              <img src={resolveAssetUrl(activeImage)} alt={listing.title} />
            ) : (
              <div className="listing-card__placeholder listing-card__placeholder--large">
                <span>{category?.name ?? "Listing"}</span>
                <strong>{listing.title}</strong>
              </div>
            )}
          </div>
          {galleryImages.length > 1 ? (
            <div className="listing-detail-gallery__thumbs">
              {galleryImages.map((image, index) => (
                <button
                  className={`listing-thumb${index === activeImageIndex ? " listing-thumb--active" : ""}`}
                  key={image}
                  type="button"
                  onClick={() => setActiveImageIndex(index)}
                >
                  <img src={resolveAssetUrl(image)} alt={`${listing.title} ${index + 1}`} />
                </button>
              ))}
            </div>
          ) : null}
        </div>

        <div className="listing-detail-copy">
          <SectionTitle
            eyebrow={category?.name ?? "Оголошення"}
            title={listing.title}
            body={listing.description}
          />
          <div className="listing-detail-stats">
            <div className="mini-stats">
              <div>
                <strong>${listing.price.toFixed(2)}</strong>
                <span>Поточна ціна</span>
              </div>
              <div>
                <strong>{listing.owner_name ?? "Продавець"}</strong>
                <span>Автор оголошення</span>
              </div>
              <div>
                <strong>{listing.created_at ? new Date(listing.created_at).toLocaleDateString() : "Нове"}</strong>
                <span>Дата публікації</span>
              </div>
            </div>
          </div>
          <div className="listing-detail-aside">
            <div className="trust-card">
              <strong>Що варто уточнити перед покупкою</strong>
              <p>Стан, комплектацію, спосіб доставки, оплату і чи є додаткові фото або відео.</p>
            </div>
            <div className="trust-card">
              <strong>Рекомендований сценарій</strong>
              <p>Перегляньте фото, порівняйте з іншими пропозиціями й одразу напишіть продавцю через вбудований чат.</p>
            </div>
          </div>
        </div>
      </section>

      {canMessageSeller && listing.owner_id ? (
        <ConversationPanel
          currentUser={user}
          recipientId={listing.owner_id}
          recipientName={listing.owner_name ?? "продавцем"}
          listingId={listing.id}
          listingTitle={listing.title}
          messages={conversationMessages}
          onSendMessage={onSendMessage}
          emptyTitle="Діалог ще не починався"
          emptyBody="Поставте перше запитання про стан товару, зустріч або доставку прямо тут."
        />
      ) : null}

      {!user ? (
        <section className="content-block">
          <div className="empty-card">
            <strong>Увійдіть, щоб написати продавцю</strong>
            <p>Доступ до внутрішнього чату відкривається після авторизації в кабінеті.</p>
            <Link className="ghost-button" to="/workspace">
              Відкрити кабінет
            </Link>
          </div>
        </section>
      ) : null}

      {relatedListings.length ? (
        <section className="content-block">
          <SectionTitle
            eyebrow="Ще в цій категорії"
            title="Схожі пропозиції, які теж можуть вам підійти"
            body="Порівняйте ціну, стан і формат подачі, перш ніж ухвалювати остаточне рішення."
          />
          <div className="listing-grid">
            {relatedListings.map((related) => (
              <Link className="related-listing-card" key={related.id} to={`/catalog/${related.id}`}>
                <div className="related-listing-card__visual">
                  {related.image_urls[0] ? (
                    <img src={resolveAssetUrl(related.image_urls[0])} alt={related.title} />
                  ) : (
                    <div className="listing-card__placeholder">
                      <span>{category?.name ?? "Listing"}</span>
                      <strong>{related.title}</strong>
                    </div>
                  )}
                </div>
                <strong>{related.title}</strong>
                <span>${related.price.toFixed(2)}</span>
              </Link>
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}
