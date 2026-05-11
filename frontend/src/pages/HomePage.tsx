import { CategorySection } from "../components/CategorySection";
import { FeatureStrip } from "../components/FeatureStrip";
import { HeroPanel } from "../components/HeroPanel";
import { ListingCard } from "../components/ListingCard";
import { StatsBar } from "../components/StatsBar";
import type { Category, Health, Listing } from "../lib/types";

interface HomePageProps {
  health: Health | null;
  categories: Category[];
  listings: Listing[];
}

export function HomePage({ health, categories, listings }: HomePageProps) {
  const featuredListings = listings.slice(0, 4);

  return (
    <div className="page-shell">
      <HeroPanel categories={categories} listings={listings} />

      <StatsBar
        metrics={[
          { label: "Active Listings", value: `${listings.length || 0}+`, description: "Live products and offers" },
          { label: "Verified Users", value: `${categories.length * 12 || 0}+`, description: "Trusted marketplace profiles" },
          { label: "Satisfaction Rate", value: health?.status === "ok" ? "98%" : "—", description: "Stable platform experience" },
          { label: "24/7 Support", value: "24/7", description: "Moderation and platform coverage" },
        ]}
      />

      <CategorySection categories={categories} listings={listings} />

      <section className="content-block home-listings-section">
        <div className="home-listings-section__header">
          <div>
            <p className="eyebrow">Fresh listings</p>
            <h3>Photo-first cards with the same premium marketplace rhythm</h3>
          </div>
        </div>
        <div className="marketplace-grid">
          {featuredListings.length ? (
            featuredListings.map((listing) => (
              <ListingCard
                key={listing.id}
                listing={listing}
                category={categories.find((category) => category.id === listing.category_id)}
              />
            ))
          ) : (
            <div className="empty-card">
              <strong>No listings yet.</strong>
              <p>Once sellers publish items, they will appear here with the updated marketplace styling.</p>
            </div>
          )}
        </div>
      </section>

      <FeatureStrip />
    </div>
  );
}
