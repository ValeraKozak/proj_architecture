import { FormEvent, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { marketplaceLocations, marketplaceTags } from "../lib/ui-demo";
import type { Category } from "../lib/types";

interface HeroSearchProps {
  categories: Category[];
}

export function HeroSearch({ categories }: HeroSearchProps) {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<"search" | "alerts">("search");
  const [query, setQuery] = useState("");
  const [categoryId, setCategoryId] = useState("");
  const [location, setLocation] = useState(marketplaceLocations[0]);
  const [maxPrice, setMaxPrice] = useState(25000);
  const [notice, setNotice] = useState("");

  const priceLabel = useMemo(() => {
    if (maxPrice >= 25000) {
      return "$0 – $25,000+";
    }
    return `$0 – $${maxPrice.toLocaleString()}`;
  }, [maxPrice]);

  function handleSubmit(event: FormEvent) {
    event.preventDefault();

    if (activeTab === "alerts") {
      setNotice("Deal alerts are not connected to the backend yet. Use Search to browse live listings.");
      return;
    }

    const params = new URLSearchParams();
    if (query.trim()) {
      params.set("query", query.trim());
    }
    if (categoryId) {
      params.set("category_id", categoryId);
    }
    if (maxPrice < 25000) {
      params.set("max_price", String(maxPrice));
    }
    if (location !== marketplaceLocations[0]) {
      params.set("location", location);
    }

    navigate(`/catalog${params.toString() ? `?${params.toString()}` : ""}`);
  }

  return (
    <div className="hero-search-card hero-search-card--panel">
      <div className="hero-search-tabs" role="tablist" aria-label="Marketplace tools">
        <button
          className={activeTab === "search" ? "active" : ""}
          type="button"
          onClick={() => {
            setActiveTab("search");
            setNotice("");
          }}
        >
          Search
        </button>
        <button
          className={activeTab === "alerts" ? "active" : ""}
          type="button"
          onClick={() => {
            setActiveTab("alerts");
            setNotice("");
          }}
        >
          Deal Alerts
        </button>
      </div>

      <form className="hero-search-form" onSubmit={handleSubmit}>
        <label>
          <span className="sr-only">Search query</span>
          <input
            placeholder={activeTab === "search" ? "What are you looking for?" : "Get notified for a search phrase"}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </label>

        <div className="hero-search-form__grid">
          <label>
            <span>Category</span>
            <select value={categoryId} onChange={(event) => setCategoryId(event.target.value)}>
              <option value="">All categories</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>Location</span>
            <select value={location} onChange={(event) => setLocation(event.target.value)}>
              {marketplaceLocations.map((entry) => (
                <option key={entry} value={entry}>
                  {entry}
                </option>
              ))}
            </select>
          </label>
        </div>

        <label className="hero-range">
          <div>
            <span>Price range</span>
            <strong>{priceLabel}</strong>
          </div>
          <input
            type="range"
            min="0"
            max="25000"
            step="250"
            value={maxPrice}
            onChange={(event) => setMaxPrice(Number(event.target.value))}
          />
        </label>

        <button className="cta-button" type="submit">
          {activeTab === "search" ? "Search Listings" : "Save Deal Alert"}
        </button>

        {notice ? <p className="hero-search-notice">{notice}</p> : null}
      </form>

      <div className="hero-tags">
        <span>Popular:</span>
        {marketplaceTags.map((tag) => (
          <button key={tag} type="button" onClick={() => setQuery(tag)}>
            {tag}
          </button>
        ))}
      </div>
    </div>
  );
}
