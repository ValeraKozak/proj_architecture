import { AuthPanel } from "../components/AuthPanel";
import { MessagesPanel } from "../components/MessagesPanel";
import { ModeratorDashboard } from "../components/ModeratorDashboard";
import { WorkspacePanels } from "../components/WorkspacePanels";
import type { Category, Listing, Message, User } from "../lib/types";
import { useSearchParams } from "react-router-dom";

interface WorkspacePageProps {
  user: User | null;
  categories: Category[];
  myListings: Listing[];
  pendingListings: Listing[];
  messages: Message[];
  onLogin: (email: string, password: string) => Promise<void>;
  onRegister: (email: string, name: string, password: string) => Promise<void>;
  onCreateListing: (payload: {
    title: string;
    description: string;
    price: number;
    category_id: number;
    image_urls: string[];
  }) => Promise<void>;
  onCreateCategory: (payload: { name: string; description: string }) => Promise<void>;
  onModerateListing: (
    listing_id: number,
    payload: { approved: boolean; rejection_reason?: string | null },
  ) => Promise<void>;
  onSendMessage: (payload: { listing_id: number; recipient_id: number; body: string }) => Promise<void>;
}

export function WorkspacePage(props: WorkspacePageProps) {
  const [searchParams] = useSearchParams();
  const authMode = searchParams.get("auth") === "register" ? "register" : "login";

  return (
    <div className="page-shell" id="workspace-overview">
      {!props.user ? (
        <section className="workspace-auth-shell">
          <div className="workspace-auth-shell__copy">
            <p className="eyebrow">Workspace access</p>
            <h2>Sign in to publish listings, review messages, and manage moderation.</h2>
            <p>
              The updated workspace keeps all of your existing CRUD, auth, and messaging logic, but
              presents it in a layout much closer to the provided reference.
            </p>
          </div>
          <AuthPanel
            initialMode={authMode}
            onLogin={props.onLogin}
            onRegister={props.onRegister}
          />
        </section>
      ) : null}

      {(props.user?.role === "moderator" || props.user?.role === "admin") ? (
        <ModeratorDashboard
          user={props.user}
          categories={props.categories}
          pendingListings={props.pendingListings}
          onModerateListing={props.onModerateListing}
        />
      ) : null}

      <MessagesPanel
        currentUser={props.user}
        listings={[...props.myListings, ...props.pendingListings]}
        messages={props.messages}
        onSendMessage={props.onSendMessage}
      />

      <section className="content-block workspace-forms-shell">
        <div className="workspace-forms-shell__header">
          <div>
            <p className="eyebrow">Seller workspace</p>
            <h3>Create listings, manage categories, and keep your current flows intact</h3>
          </div>
        </div>
        <WorkspacePanels
          user={props.user}
          categories={props.categories}
          myListings={props.myListings}
          pendingListings={props.pendingListings}
          messages={props.messages}
          onCreateListing={props.onCreateListing}
          onCreateCategory={props.onCreateCategory}
          onModerateListing={props.onModerateListing}
        />
      </section>
    </div>
  );
}
