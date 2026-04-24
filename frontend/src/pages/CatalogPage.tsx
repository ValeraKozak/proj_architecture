import type { Category, Listing } from "../lib/types";
import { ListingCard } from "../components/ListingCard";
import { SectionTitle } from "../components/SectionTitle";

interface CatalogPageProps {
  categories: Category[];
  listings: Listing[];
}

export function CatalogPage({ categories, listings }: CatalogPageProps) {
  return (
    <div className="page-shell">
      <section className="content-block split-layout">
        <div className="catalog-sidebar">
          <SectionTitle
            eyebrow="Inventory map"
            title="Category overview"
            body="The left rail doubles as a visual category navigator and a quick project-proof that the backend categorization model is usable in UI."
          />
          <div className="category-column">
            {categories.length ? (
              categories.map((category) => (
                <div className="category-pill" key={category.id}>
                  <strong>{category.name}</strong>
                  <span>{category.description}</span>
                </div>
              ))
            ) : (
              <div className="empty-card">
                <strong>No categories yet</strong>
                <p>Create one from the workspace or admin API.</p>
              </div>
            )}
          </div>
        </div>
        <div className="catalog-main">
          <SectionTitle
            eyebrow="Listings"
            title="Marketplace board"
            body="Public approved listings are shown with richer visual framing than the backend docs, which helps the project feel like a product instead of just an API demo."
          />
          <div className="listing-grid">
            {listings.length ? (
              listings.map((listing) => (
                <ListingCard
                  key={listing.id}
                  listing={listing}
                  category={categories.find((category) => category.id === listing.category_id)}
                />
              ))
            ) : (
              <div className="empty-card">
                <strong>No approved listings available</strong>
                <p>Use moderation endpoints to approve new content and populate this board.</p>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
