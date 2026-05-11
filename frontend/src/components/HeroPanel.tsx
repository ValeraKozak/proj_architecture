import { resolveAssetUrl } from "../lib/api";
import type { Category, Listing } from "../lib/types";
import { HeroSearch } from "./HeroSearch";

interface HeroPanelProps {
  categories: Category[];
  listings: Listing[];
}

export function HeroPanel({ categories, listings }: HeroPanelProps) {
  const featured = listings.slice(0, 5);

  return (
    <section className="hero-marketplace">
      <div className="hero-marketplace__left">
        <div>
          <p className="hero-marketplace__eyebrow">Modern marketplace for real people</p>
          <h1>
            Buy. Sell.
            <br />
            Connect.
          </h1>
          <p className="hero-marketplace__body">
            A cleaner bulletin board platform with curated listings, fast browse, and a calmer way
            to connect buyers with sellers.
          </p>
        </div>

        <HeroSearch categories={categories} />
      </div>

      <div className="hero-marketplace__right">
        <div className="hero-visual-grid">
          {featured.map((listing, index) => (
            <article className={`hero-visual-card hero-visual-card--${index + 1}`} key={listing.id}>
              <div className="hero-visual-card__image">
                {listing.image_urls[0] ? (
                  <img alt={listing.title} src={resolveAssetUrl(listing.image_urls[0])} />
                ) : (
                  <div className="hero-visual-card__placeholder">
                    <span>{listing.title.slice(0, 18)}</span>
                  </div>
                )}
              </div>
              <div className="hero-visual-card__overlay">
                <strong className="line-clamp-2">{listing.title}</strong>
                <span>${listing.price.toFixed(0)}</span>
                <small>
                  {listing.created_at ? new Date(listing.created_at).toLocaleDateString() : "Today"}
                </small>
              </div>
            </article>
          ))}

          <div className="hero-verified-badge">
            <span>Verified Seller</span>
            <strong>Quality listing</strong>
          </div>
        </div>
      </div>
    </section>
  );
}
