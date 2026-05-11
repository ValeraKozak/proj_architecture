import { FormEvent, useMemo, useState } from "react";

import type { Message, User } from "../lib/types";

interface ConversationPanelProps {
  currentUser: User | null;
  recipientId: number;
  recipientName: string;
  listingId: number;
  listingTitle: string;
  messages: Message[];
  onSendMessage: (payload: { listing_id: number; recipient_id: number; body: string }) => Promise<void>;
  emptyTitle: string;
  emptyBody: string;
}

export function ConversationPanel({
  currentUser,
  recipientId,
  recipientName,
  listingId,
  listingTitle,
  messages,
  onSendMessage,
  emptyTitle,
  emptyBody,
}: ConversationPanelProps) {
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const orderedMessages = useMemo(
    () =>
      [...messages].sort((left, right) => {
        const leftTime = left.created_at ? new Date(left.created_at).getTime() : 0;
        const rightTime = right.created_at ? new Date(right.created_at).getTime() : 0;
        return leftTime - rightTime;
      }),
    [messages],
  );

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setSuccess("");

    if (!currentUser) {
      setError("Увійдіть у систему, щоб почати діалог.");
      return;
    }
    if (draft.trim().length < 2) {
      setError("Повідомлення має містити щонайменше 2 символи.");
      return;
    }

    setBusy(true);
    try {
      await onSendMessage({
        listing_id: listingId,
        recipient_id: recipientId,
        body: draft.trim(),
      });
      setDraft("");
      setSuccess("Повідомлення надіслано.");
    } catch (submissionError) {
      setError(
        submissionError instanceof Error
          ? submissionError.message
          : "Не вдалося надіслати повідомлення.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="conversation-panel">
      <div className="conversation-panel__header">
        <div>
          <span className="eyebrow">Повідомлення</span>
          <h3>Діалог щодо “{listingTitle}”</h3>
          <p>Спілкування між вами та {recipientName} без виходу за межі платформи.</p>
        </div>
        <span className="status-pill">З {recipientName}</span>
      </div>

      <div className="conversation-thread">
        {orderedMessages.length ? (
          orderedMessages.map((message) => {
            const outgoing = currentUser?.id === message.sender_id;
            return (
              <article
                className={`message-bubble${outgoing ? " message-bubble--outgoing" : ""}`}
                key={message.id}
              >
                <div className="message-bubble__meta">
                  <strong>
                    {outgoing
                      ? "Ви"
                      : message.sender_name ?? message.recipient_name ?? recipientName}
                  </strong>
                  <span>
                    {message.created_at
                      ? new Date(message.created_at).toLocaleString()
                      : "щойно"}
                  </span>
                </div>
                <p>{message.body}</p>
              </article>
            );
          })
        ) : (
          <div className="empty-card">
            <strong>{emptyTitle}</strong>
            <p>{emptyBody}</p>
          </div>
        )}
      </div>

      <form className="stack-form conversation-panel__form" onSubmit={handleSubmit}>
        <label>
          Нове повідомлення
          <textarea
            value={draft}
            placeholder="Напишіть продавцю або покупцю уточнення щодо товару, доставки чи стану."
            onChange={(event) => setDraft(event.target.value)}
          />
        </label>
        <button className="cta-button" disabled={busy} type="submit">
          {busy ? "Надсилаємо..." : "Надіслати повідомлення"}
        </button>
        {error ? <p className="form-error">{error}</p> : null}
        {success ? <p className="form-success">{success}</p> : null}
      </form>
    </section>
  );
}
