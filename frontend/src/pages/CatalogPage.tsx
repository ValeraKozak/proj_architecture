import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { ListingCard } from "../components/ListingCard";
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
  const [searchParams, setSearchParams] = useSearchParams();
  const [filters, setFilters] = useState({
    query: searchParams.get("query") ?? "",
    category_id: searchParams.get("category_id") ?? "",
    min_price: searchParams.get("min_price") ?? "",
    max_price: searchParams.get("max_price") ?? "",
    sort_by: (searchParams.get("sort_by") as "created_at" | "price") ?? DEFAULT_FILTERS.sort_by,
    sort_order: (searchParams.get("sort_order") as "asc" | "desc") ?? DEFAULT_FILTERS.sort_order,
    location: searchParams.get("location") ?? "All locations",
  });
  const [listings, setListings] = useState<Listing[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value && value !== "All locations") {
        params.set(key, value);
      }
    });
    setSearchParams(params, { replace: true });
  }, [filters, setSearchParams]);

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

  const activeCategory = useMemo(
    () => categories.find((category) => String(category.id) === filters.category_id),
    [categories, filters.category_id],
  );

  return (
    <div className="page-shell">
      <section className="catalog-shell">
        <aside className="catalog-sidebar-modern">
          <p className="eyebrow">Browse marketplace</p>
          <h2>Search listings with the same calm flow as the reference design</h2>

          <form className="catalog-filters-modern">
            <label>
              Search
              <input
                placeholder="Camera, apartment, bike..."
                value={filters.query}
                onChange={(event) => setFilters((current) => ({ ...current, query: event.target.value }))}
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
            <div className="catalog-filters-modern__row">
              <label>
                Min price
                <input
                  min="0"
                  type="number"
                  value={filters.min_price}
                  onChange={(event) => setFilters((current) => ({ ...current, min_price: event.target.value }))}
                />
              </label>
              <label>
                Max price
                <input
                  min="0"
                  type="number"
                  value={filters.max_price}
                  onChange={(event) => setFilters((current) => ({ ...current, max_price: event.target.value }))}
                />
              </label>
            </div>
            <div className="catalog-filters-modern__row">
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
                  <option value="created_at">Newest</option>
                  <option value="price">Price</option>
                </select>
              </label>
              <label>
                Order
                <select
                  value={filters.sort_order}
                  onChange={(event) =>
                    setFilters((current) => ({ ...current, sort_order: event.target.value as "asc" | "desc" }))
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
                  location: "All locations",
                })
              }
            >
              Reset filters
            </button>
          </form>

          <div className="catalog-category-list">
            {categories.map((category) => (
              <button
                className={String(category.id) === filters.category_id ? "active" : ""}
                key={category.id}
                type="button"
                onClick={() =>
                  setFilters((current) => ({
                    ...current,
                    category_id: current.category_id === String(category.id) ? "" : String(category.id),
                  }))
                }
              >
                {category.name}
              </button>
            ))}
          </div>
        </aside>

        <div className="catalog-main-modern">
          <div className="catalog-main-modern__header">
            <div>
              <p className="eyebrow">Listing results</p>
              <h2>{activeCategory?.name ?? "All listings"}</h2>
            </div>
            <div className="catalog-meta">
              <strong>{isLoading ? "Loading..." : `${listings.length} results`}</strong>
              <span>{filters.location}</span>
            </div>
          </div>

          {error ? <p className="form-error">{error}</p> : null}

          <div className="marketplace-grid">
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
                <strong>{isLoading ? "Refreshing listings..." : "No listings found."}</strong>
                <p>
                  {isLoading
                    ? "The catalog is fetching live data from the current API."
                    : "Try a wider search phrase or clear one of the active filters."}
                </p>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
