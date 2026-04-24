import type { Category, Listing } from "../lib/types";

interface ListingCardProps {
  listing: Listing;
  category?: Category;
}

export function ListingCard({ listing, category }: ListingCardProps) {
  const coverImage = listing.image_urls[0];

  return (
    <article className="listing-card">
      <div className="listing-card__visual">
        {coverImage ? (
          <img src={coverImage} alt={listing.title} />
        ) : (
          <div className="listing-card__placeholder">
            <span>{category?.name ?? "Listing"}</span>
            <strong>{listing.title}</strong>
          </div>
        )}
      </div>
      <div className="listing-card__meta">
        <span>{category?.name ?? "Uncategorized"}</span>
        <span className={`status-badge ${listing.status}`}>{listing.status}</span>
      </div>
      <h4>{listing.title}</h4>
      <p>{listing.description}</p>
      {listing.image_urls.length > 1 ? (
        <div className="listing-card__gallery-count">+{listing.image_urls.length - 1} more images</div>
      ) : null}
      <div className="listing-card__footer">
        <strong>${listing.price.toFixed(2)}</strong>
        <small>{listing.created_at ? new Date(listing.created_at).toLocaleDateString() : "Draft"}</small>
      </div>
    </article>
  );
}
