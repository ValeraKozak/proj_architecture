import { FormEvent, useEffect, useMemo, useState } from "react";

import { resolveAssetUrl } from "../lib/api";
import type { Listing, Message, User } from "../lib/types";

interface MessagesPanelProps {
  currentUser: User | null;
  listings: Listing[];
  messages: Message[];
  onSendMessage: (payload: { listing_id: number; recipient_id: number; body: string }) => Promise<void>;
}

export function MessagesPanel({ currentUser, listings, messages, onSendMessage }: MessagesPanelProps) {
  const [activeThreadKey, setActiveThreadKey] = useState("");
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [feedback, setFeedback] = useState("");

  const threads = useMemo(() => {
    if (!currentUser) {
      return [];
    }

    const groups = new Map<
      string,
      {
        key: string;
        listingId: number;
        listingTitle: string;
        recipientId: number;
        recipientName: string;
        preview: string;
        lastAt: number;
        thumbnail?: string;
        messages: Message[];
      }
    >();

    for (const message of messages) {
      const otherId = message.sender_id === currentUser.id ? message.recipient_id : message.sender_id;
      const otherName =
        message.sender_id === currentUser.id
          ? message.recipient_name ?? "Buyer"
          : message.sender_name ?? "Seller";
      const key = `${message.listing_id}-${otherId}`;
      const relatedListing = listings.find((listing) => listing.id === message.listing_id);
      const createdAt = message.created_at ? new Date(message.created_at).getTime() : 0;

      const current = groups.get(key);
      if (!current) {
        groups.set(key, {
          key,
          listingId: message.listing_id,
          listingTitle: relatedListing?.title ?? `Listing #${message.listing_id}`,
          recipientId: otherId,
          recipientName: otherName,
          preview: message.body,
          lastAt: createdAt,
          thumbnail: relatedListing?.image_urls[0],
          messages: [message],
        });
      } else {
        current.messages.push(message);
        if (createdAt >= current.lastAt) {
          current.preview = message.body;
          current.lastAt = createdAt;
        }
      }
    }

    return [...groups.values()].sort((left, right) => right.lastAt - left.lastAt);
  }, [currentUser, listings, messages]);

  useEffect(() => {
    if (!threads.length) {
      setActiveThreadKey("");
      return;
    }

    if (!activeThreadKey || !threads.some((thread) => thread.key === activeThreadKey)) {
      setActiveThreadKey(threads[0].key);
    }
  }, [activeThreadKey, threads]);

  const activeThread = threads.find((thread) => thread.key === activeThreadKey) ?? null;
  const activeMessages = useMemo(() => {
    if (!activeThread) {
      return [];
    }
    return [...activeThread.messages].sort((left, right) => {
      const leftTime = left.created_at ? new Date(left.created_at).getTime() : 0;
      const rightTime = right.created_at ? new Date(right.created_at).getTime() : 0;
      return leftTime - rightTime;
    });
  }, [activeThread]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!currentUser || !activeThread || draft.trim().length < 2) {
      return;
    }

    setBusy(true);
    setFeedback("");
    try {
      await onSendMessage({
        listing_id: activeThread.listingId,
        recipient_id: activeThread.recipientId,
        body: draft.trim(),
      });
      setDraft("");
    } catch (error) {
      setFeedback(error instanceof Error ? error.message : "Message failed to send.");
    } finally {
      setBusy(false);
    }
  }

  if (!currentUser) {
    return (
      <section className="messages-shell">
        <div className="empty-card">
          <strong>Sign in to open your message center.</strong>
          <p>Your listing conversations will appear here once you log in and start chatting with buyers or sellers.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="messages-shell">
      <div className="messages-list">
        <div className="messages-list__header">
          <strong>Messages</strong>
          <span>{threads.length}</span>
        </div>
        <label className="messages-search">
          <span className="sr-only">Search messages</span>
          <input placeholder="Search messages" />
        </label>
        <div className="messages-list__items">
          {threads.length ? (
            threads.map((thread) => (
              <button
                className={`message-thread-card${thread.key === activeThreadKey ? " active" : ""}`}
                key={thread.key}
                type="button"
                onClick={() => setActiveThreadKey(thread.key)}
              >
                <strong>{thread.recipientName}</strong>
                <span>{thread.preview}</span>
              </button>
            ))
          ) : (
            <div className="empty-card">
              <strong>No conversations yet.</strong>
              <p>Start from a listing page and your active threads will appear here.</p>
            </div>
          )}
        </div>
      </div>

      <div className="messages-chat">
        {activeThread ? (
          <>
            <div className="messages-chat__header">
              <div>
                <strong>{activeThread.recipientName}</strong>
                <span>Active conversation</span>
              </div>
            </div>
            <div className="messages-chat__listing">
              <div className="messages-chat__listing-image">
                {activeThread.thumbnail ? (
                  <img src={resolveAssetUrl(activeThread.thumbnail)} alt={activeThread.listingTitle} />
                ) : (
                  <div />
                )}
              </div>
              <div>
                <strong>{activeThread.listingTitle}</strong>
                <span>View listing</span>
              </div>
            </div>
            <div className="messages-bubbles">
              {activeMessages.map((message) => {
                const outgoing = message.sender_id === currentUser.id;
                return (
                  <article className={`messages-bubble${outgoing ? " outgoing" : ""}`} key={message.id}>
                    <p>{message.body}</p>
                    <small>
                      {message.created_at ? new Date(message.created_at).toLocaleTimeString() : "now"}
                    </small>
                  </article>
                );
              })}
            </div>
            <form className="messages-compose" onSubmit={handleSubmit}>
              <input
                placeholder="Type a message..."
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
              />
              <button className="cta-button" disabled={busy} type="submit">
                {busy ? "Sending..." : "Send"}
              </button>
            </form>
            {feedback ? <p className="form-error">{feedback}</p> : null}
          </>
        ) : (
          <div className="empty-card">
            <strong>Select a conversation.</strong>
            <p>Your active marketplace chats will render here with the connected listing context.</p>
          </div>
        )}
      </div>
    </section>
  );
}
