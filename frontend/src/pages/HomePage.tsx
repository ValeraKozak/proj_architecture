import type { Category, Health, Listing } from "../lib/types";
import { HeroPanel } from "../components/HeroPanel";
import { ListingCard } from "../components/ListingCard";
import { MetricStrip } from "../components/MetricStrip";
import { SectionTitle } from "../components/SectionTitle";

interface HomePageProps {
  health: Health | null;
  categories: Category[];
  listings: Listing[];
}

export function HomePage({ health, categories, listings }: HomePageProps) {
  return (
    <div className="page-shell">
      <HeroPanel />
      <MetricStrip
        metrics={[
          { label: "API status", value: health?.status ?? "loading", tone: "mint" },
          { label: "Categories", value: String(categories.length), tone: "sand" },
          { label: "Public listings", value: String(listings.length), tone: "coral" },
        ]}
      />
      <section className="content-block">
        <SectionTitle
          eyebrow="Catalog pulse"
          title="Public storefront"
          body="Live approved listings from the backend. If the database is still empty, the layout keeps the page looking deliberate rather than broken."
        />
        <div className="listing-grid">
          {listings.length ? (
            listings.slice(0, 6).map((listing) => (
              <ListingCard
                key={listing.id}
                listing={listing}
                category={categories.find((category) => category.id === listing.category_id)}
              />
            ))
          ) : (
            <div className="empty-card hero-empty">
              <strong>Catalog is ready for data</strong>
              <p>
                The frontend is connected. Add categories and publish listings through Swagger or the
                workspace panel to make the storefront come alive.
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
