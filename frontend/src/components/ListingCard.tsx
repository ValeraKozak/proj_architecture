import { Link } from "react-router-dom";

import { resolveAssetUrl } from "../lib/api";
import type { Category, Listing } from "../lib/types";

interface ListingCardProps {
  listing: Listing;
  category?: Category;
}

const statusLabels: Record<Listing["status"], string> = {
  approved: "Verified Seller",
  pending: "Needs Review",
  rejected: "Rejected",
  draft: "Draft",
  archived: "Archived",
};

export function ListingCard({ listing, category }: ListingCardProps) {
  return (
    <article className="marketplace-card">
      <Link className="marketplace-card__link" to={`/catalog/${listing.id}`}>
        <div className="marketplace-card__image">
          {listing.image_urls[0] ? (
            <img src={resolveAssetUrl(listing.image_urls[0])} alt={listing.title} />
          ) : (
            <div className="marketplace-card__placeholder">
              <span>{category?.name ?? "Listing"}</span>
            </div>
          )}
          <span className="marketplace-card__badge">{statusLabels[listing.status]}</span>
        </div>
        <div className="marketplace-card__body">
          <div className="marketplace-card__topline">
            <span className="line-clamp-1">{category?.name ?? "General"}</span>
            <small className="line-clamp-1">
              {listing.created_at ? new Date(listing.created_at).toLocaleDateString() : "New"}
            </small>
          </div>
          <strong className="line-clamp-2">{listing.title}</strong>
          <p className="line-clamp-3">
            {listing.description.slice(0, 148)}
            {listing.description.length > 148 ? "..." : ""}
          </p>
          <div className="marketplace-card__footer">
            <span className="line-clamp-1">${listing.price.toFixed(2)}</span>
            <small className="line-clamp-1">{listing.owner_name ?? "Marketplace seller"}</small>
          </div>
        </div>
      </Link>
    </article>
  );
}
