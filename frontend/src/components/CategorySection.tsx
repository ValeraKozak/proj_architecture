import { Link } from "react-router-dom";

import { resolveAssetUrl } from "../lib/api";
import type { Category, Listing } from "../lib/types";

interface CategorySectionProps {
  categories: Category[];
  listings: Listing[];
}

const featuredCategoryNames = ["Vehicles", "Property", "Electronics", "Home & Garden"];

function matchCategoryVisual(category: Category, listings: Listing[]) {
  return listings.find((listing) => listing.category_id === category.id && listing.image_urls[0]);
}

export function CategorySection({ categories, listings }: CategorySectionProps) {
  const featured = categories.slice(0, 4);
  const sidebar = categories.slice(0, 8);

  return (
    <section className="category-section content-block" id="categories">
      <div className="category-section__header">
        <div>
          <p className="eyebrow">Explore by category</p>
          <h3>Browse listings with the same calm structure as the reference design</h3>
        </div>
        <Link className="text-link" to="/catalog">
          View all categories
        </Link>
      </div>

      <div className="category-section__layout">
        <aside className="category-menu">
          <button className="category-menu__active" type="button">
            For You
          </button>
          {sidebar.map((category) => (
            <Link key={category.id} to={`/catalog?category_id=${category.id}`}>
              {category.name}
            </Link>
          ))}
        </aside>

        <div className="category-grid">
          {featured.map((category, index) => {
            const visual = matchCategoryVisual(category, listings);
            return (
              <Link className="category-showcase-card" key={category.id} to={`/catalog?category_id=${category.id}`}>
                <div className="category-showcase-card__visual">
                  {visual?.image_urls[0] ? (
                    <img src={resolveAssetUrl(visual.image_urls[0])} alt={category.name} />
                  ) : (
                    <div className="category-showcase-card__placeholder">
                      <span>{featuredCategoryNames[index] ?? category.name}</span>
                    </div>
                  )}
                </div>
                <div className="category-showcase-card__copy">
                  <strong className="line-clamp-2">{featuredCategoryNames[index] ?? category.name}</strong>
                  <span>{listings.filter((listing) => listing.category_id === category.id).length} listings</span>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
}
