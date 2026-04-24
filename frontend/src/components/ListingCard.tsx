import type { Category, Listing } from "../lib/types";

interface ListingCardProps {
  listing: Listing;
  category?: Category;
}

export function ListingCard({ listing, category }: ListingCardProps) {
  return (
    <article className="listing-card">
      <div className="listing-card__meta">
        <span>{category?.name ?? "Uncategorized"}</span>
        <span className={`status-badge ${listing.status}`}>{listing.status}</span>
      </div>
      <h4>{listing.title}</h4>
      <p>{listing.description}</p>
      <div className="listing-card__footer">
        <strong>${listing.price.toFixed(2)}</strong>
        <small>{listing.created_at ? new Date(listing.created_at).toLocaleDateString() : "Draft"}</small>
      </div>
    </article>
  );
}
