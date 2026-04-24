import { useEffect, useState } from "react";

import { ListingCard } from "../components/ListingCard";
import { SectionTitle } from "../components/SectionTitle";
import { api } from "../lib/api";
import type { Category, Listing, ListingFilters } from "../lib/types";

interface CatalogPageProps {
  categories: Category[];
}

const DEFAULT_FILTERS: Required<Pick<ListingFilters, "sort_by" | "sort_order">> = {
  sort_by: "created_at",
  sort_order: "desc",
};

export function CatalogPage({ categories }: CatalogPageProps) {
  const [filters, setFilters] = useState({
    query: "",
    category_id: "",
    min_price: "",
    max_price: "",
    sort_by: DEFAULT_FILTERS.sort_by,
    sort_order: DEFAULT_FILTERS.sort_order,
  });
  const [listings, setListings] = useState<Listing[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => {
      setIsLoading(true);
      setError("");
      api
        .listings({
          query: filters.query || undefined,
          category_id: filters.category_id ? Number(filters.category_id) : undefined,
          min_price: filters.min_price ? Number(filters.min_price) : undefined,
          max_price: filters.max_price ? Number(filters.max_price) : undefined,
          sort_by: filters.sort_by,
          sort_order: filters.sort_order,
        })
        .then((result) => {
          if (!controller.signal.aborted) {
            setListings(result);
          }
        })
        .catch((loadError) => {
          if (!controller.signal.aborted) {
            setError(loadError instanceof Error ? loadError.message : "Failed to load listings.");
            setListings([]);
          }
        })
        .finally(() => {
          if (!controller.signal.aborted) {
            setIsLoading(false);
          }
        });
    }, 180);

    return () => {
      controller.abort();
      window.clearTimeout(timeoutId);
    };
  }, [filters]);

  return (
    <div className="page-shell">
      <section className="content-block split-layout">
        <div className="catalog-sidebar">
          <SectionTitle
            eyebrow="Inventory map"
            title="Search and filter board"
            body="The catalog now behaves like a real storefront: live query matching, category filtering, price ranges and sorting all run against the API."
          />
          <form className="stack-form catalog-filter-panel">
            <label>
              Search
              <input
                placeholder="camera, chair, electronics..."
                value={filters.query}
                onChange={(event) =>
                  setFilters((current) => ({ ...current, query: event.target.value }))
                }
              />
            </label>
            <label>
              Category
              <select
                value={filters.category_id}
                onChange={(event) =>
                  setFilters((current) => ({ ...current, category_id: event.target.value }))
                }
              >
                <option value="">All categories</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </label>
            <div className="form-row">
              <label>
                Min price
                <input
                  type="number"
                  min="0"
                  value={filters.min_price}
                  onChange={(event) =>
                    setFilters((current) => ({ ...current, min_price: event.target.value }))
                  }
                />
              </label>
              <label>
                Max price
                <input
                  type="number"
                  min="0"
                  value={filters.max_price}
                  onChange={(event) =>
                    setFilters((current) => ({ ...current, max_price: event.target.value }))
                  }
                />
              </label>
            </div>
            <div className="form-row">
              <label>
                Sort by
                <select
                  value={filters.sort_by}
                  onChange={(event) =>
                    setFilters((current) => ({
                      ...current,
                      sort_by: event.target.value as "created_at" | "price",
                    }))
                  }
                >
                  <option value="created_at">Newest first</option>
                  <option value="price">Price</option>
                </select>
              </label>
              <label>
                Order
                <select
                  value={filters.sort_order}
                  onChange={(event) =>
                    setFilters((current) => ({
                      ...current,
                      sort_order: event.target.value as "asc" | "desc",
                    }))
                  }
                >
                  <option value="desc">Descending</option>
                  <option value="asc">Ascending</option>
                </select>
              </label>
            </div>
            <button
              className="ghost-button"
              type="button"
              onClick={() =>
                setFilters({
                  query: "",
                  category_id: "",
                  min_price: "",
                  max_price: "",
                  sort_by: DEFAULT_FILTERS.sort_by,
                  sort_order: DEFAULT_FILTERS.sort_order,
                })
              }
            >
              Reset filters
            </button>
          </form>
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
            title="Filtered marketplace board"
            body="Approved listings now render through a proper search experience, with large visual cards and server-side filtering instead of a static dump."
          />
          {error ? <p className="form-error">{error}</p> : null}
          <div className="catalog-results-bar">
            <strong>{isLoading ? "Loading..." : `${listings.length} matches`}</strong>
            <span>Search, category, price range and sorting are all backed by the API.</span>
          </div>
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
                <strong>{isLoading ? "Refreshing catalog" : "No listings match this filter set"}</strong>
                <p>
                  {isLoading
                    ? "The board is pulling fresh API data."
                    : "Try widening the price range, changing the search query or clearing the category filter."}
                </p>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
