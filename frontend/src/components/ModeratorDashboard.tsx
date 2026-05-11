import { useMemo, useState } from "react";

import { resolveAssetUrl } from "../lib/api";
import type { Category, Listing, User } from "../lib/types";
import { moderationNavItems, workspaceNavItems } from "../lib/ui-demo";

interface ModeratorDashboardProps {
  user: User | null;
  categories: Category[];
  pendingListings: Listing[];
  onModerateListing: (
    listing_id: number,
    payload: { approved: boolean; rejection_reason?: string | null },
  ) => Promise<void>;
}

type QueueTab = "all" | "new" | "needs-review" | "reported";

export function ModeratorDashboard({
  user,
  categories,
  pendingListings,
  onModerateListing,
}: ModeratorDashboardProps) {
  const [activeTab, setActiveTab] = useState<QueueTab>("all");
  const [sortOrder, setSortOrder] = useState<"newest" | "price-high" | "price-low">("newest");
  const [busyId, setBusyId] = useState<number | null>(null);
  const [rejectionNotes, setRejectionNotes] = useState<Record<number, string>>({});
  const [feedback, setFeedback] = useState("");

  const canModerate = user?.role === "moderator" || user?.role === "admin";
  const categoryMap = useMemo(
    () => new Map(categories.map((category) => [category.id, category.name])),
    [categories],
  );

  const taggedListings = useMemo(
    () =>
      pendingListings.map((listing, index) => ({
        listing,
        bucket:
          index % 4 === 0
            ? "reported"
            : listing.description.length < 80
              ? "needs-review"
              : index % 2 === 0
                ? "new"
                : "all",
      })),
    [pendingListings],
  );

  const filteredListings = useMemo(() => {
    const scoped = taggedListings.filter((entry) => {
      if (activeTab === "all") {
        return true;
      }
      return entry.bucket === activeTab;
    });

    const sortable = [...scoped];
    sortable.sort((left, right) => {
      if (sortOrder === "price-high") {
        return right.listing.price - left.listing.price;
      }
      if (sortOrder === "price-low") {
        return left.listing.price - right.listing.price;
      }

      const leftTime = left.listing.created_at ? new Date(left.listing.created_at).getTime() : 0;
      const rightTime = right.listing.created_at ? new Date(right.listing.created_at).getTime() : 0;
      return rightTime - leftTime;
    });
    return sortable;
  }, [activeTab, sortOrder, taggedListings]);

  async function moderate(listingId: number, approved: boolean) {
    if (!canModerate) {
      setFeedback("Moderation actions are available only for moderator and admin accounts.");
      return;
    }

    const note = rejectionNotes[listingId]?.trim() ?? "";
    if (!approved && note.length < 5) {
      setFeedback("Please add at least 5 characters when declining a listing.");
      return;
    }

    setBusyId(listingId);
    setFeedback("");
    try {
      await onModerateListing(listingId, {
        approved,
        rejection_reason: approved ? null : note,
      });
      setFeedback(approved ? "Listing approved successfully." : "Listing declined with feedback.");
      setRejectionNotes((current) => {
        const next = { ...current };
        delete next[listingId];
        return next;
      });
    } catch (error) {
      setFeedback(error instanceof Error ? error.message : "Moderation action failed.");
    } finally {
      setBusyId(null);
    }
  }

  const tabCounts = {
    all: pendingListings.length,
    new: taggedListings.filter((entry) => entry.bucket === "new").length,
    "needs-review": taggedListings.filter((entry) => entry.bucket === "needs-review").length,
    reported: taggedListings.filter((entry) => entry.bucket === "reported").length,
  };

  return (
    <section className="dashboard-shell" id="how-it-works">
      <aside className="dashboard-sidebar">
        <div className="dashboard-sidebar__brand">BB</div>
        <nav className="dashboard-sidebar__nav">
          {workspaceNavItems.map((item, index) => (
            <a className={index === 0 ? "active" : ""} href="#workspace-overview" key={item}>
              {item}
            </a>
          ))}
        </nav>
        <div className="dashboard-sidebar__divider" />
        <div className="dashboard-sidebar__label">Moderation</div>
        <nav className="dashboard-sidebar__nav dashboard-sidebar__nav--secondary">
          {moderationNavItems.map((item, index) => (
            <a className={index === 0 ? "active" : ""} href="#moderation-queue" key={item}>
              {item}
            </a>
          ))}
        </nav>
        <div className="dashboard-sidebar__profile">
          <strong>{user?.full_name ?? "Alex Morgan"}</strong>
          <span>{user?.role ?? "Moderator"}</span>
        </div>
      </aside>

      <div className="dashboard-main" id="moderation-queue">
        <div className="dashboard-main__header">
          <div>
            <h3>Moderation Queue</h3>
            <p>Review and take action on pending listings.</p>
          </div>
          <div className="dashboard-toolbar">
            <button className="ghost-button" type="button">
              Filters
            </button>
            <select value={sortOrder} onChange={(event) => setSortOrder(event.target.value as typeof sortOrder)}>
              <option value="newest">Newest</option>
              <option value="price-high">Price high</option>
              <option value="price-low">Price low</option>
            </select>
          </div>
        </div>

        <div className="dashboard-tabs">
          <button className={activeTab === "all" ? "active" : ""} type="button" onClick={() => setActiveTab("all")}>
            All ({tabCounts.all})
          </button>
          <button className={activeTab === "new" ? "active" : ""} type="button" onClick={() => setActiveTab("new")}>
            New ({tabCounts.new})
          </button>
          <button
            className={activeTab === "needs-review" ? "active" : ""}
            type="button"
            onClick={() => setActiveTab("needs-review")}
          >
            Needs Review ({tabCounts["needs-review"]})
          </button>
          <button
            className={activeTab === "reported" ? "active" : ""}
            type="button"
            onClick={() => setActiveTab("reported")}
          >
            Reported ({tabCounts.reported})
          </button>
        </div>

        {feedback ? <p className="form-success">{feedback}</p> : null}

        <div className="queue-list">
          {filteredListings.length ? (
            filteredListings.map(({ listing, bucket }) => (
              <article className="queue-card" key={listing.id}>
                <div className="queue-card__media">
                  {listing.image_urls[0] ? (
                    <img alt={listing.title} src={resolveAssetUrl(listing.image_urls[0])} />
                  ) : (
                    <div />
                  )}
                </div>
                <div className="queue-card__copy">
                  <strong>{listing.title}</strong>
                  <span>${listing.price.toFixed(0)}</span>
                  <small>
                    {categoryMap.get(listing.category_id) ?? "General"} · {bucket.replace("-", " ")}
                  </small>
                </div>
                <label className="queue-card__note">
                  <span className="sr-only">Decline note</span>
                  <input
                    placeholder="Optional decline note"
                    value={rejectionNotes[listing.id] ?? ""}
                    onChange={(event) =>
                      setRejectionNotes((current) => ({ ...current, [listing.id]: event.target.value }))
                    }
                  />
                </label>
                <div className="queue-card__actions">
                  <button
                    className="cta-button"
                    type="button"
                    disabled={busyId === listing.id}
                    onClick={() => void moderate(listing.id, true)}
                  >
                    {busyId === listing.id ? "Working..." : "Approve"}
                  </button>
                  <button
                    className="ghost-button"
                    type="button"
                    disabled={busyId === listing.id}
                    onClick={() => void moderate(listing.id, false)}
                  >
                    {busyId === listing.id ? "Working..." : "Decline"}
                  </button>
                </div>
              </article>
            ))
          ) : (
            <div className="empty-card">
              <strong>No listings in this queue right now.</strong>
              <p>New moderation items will appear here automatically when sellers publish new ads.</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
