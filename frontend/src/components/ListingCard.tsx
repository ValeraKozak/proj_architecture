import type { Category, Listing } from "../lib/types";

interface ListingCardProps {
  listing: Listing;
  category?: Category;
}

export function ListingCard({ listing, category }: ListingCardProps) {
  const descriptionPreview =
    listing.description.length > 120
      ? `${listing.description.slice(0, 117)}...`
      : listing.description;
  const statusLabels: Record<Listing["status"], string> = {
    approved: "схвалено",
    pending: "модерація",
    rejected: "відхилено",
    draft: "чернетка",
    archived: "архів",
  };

  return (
    <article className="listing-card">
      <div className="listing-card__visual">
        <div className="listing-card__placeholder">
          <span>{category?.name ?? "Listing"}</span>
          <strong>{listing.title}</strong>
        </div>
      </div>
      <div className="listing-card__meta">
        <span>{category?.name ?? "Uncategorized"}</span>
        <span className={`status-badge ${listing.status}`}>{statusLabels[listing.status]}</span>
      </div>
      <h4>{listing.title}</h4>
      <p>{descriptionPreview}</p>
      {listing.image_urls.length > 1 ? (
        <div className="listing-card__gallery-count">
          +{listing.image_urls.length - 1} додаткових фото
        </div>
      ) : null}
      <div className="listing-card__footer">
        <strong>${listing.price.toFixed(2)}</strong>
        <small>
          {listing.created_at ? new Date(listing.created_at).toLocaleDateString() : "Чернетка"}
        </small>
      </div>
    </article>
  );
}
