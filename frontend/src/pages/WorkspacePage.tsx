import type { Category, Listing, Message, User } from "../lib/types";
import { AuthPanel } from "../components/AuthPanel";
import { MetricStrip } from "../components/MetricStrip";
import { SectionTitle } from "../components/SectionTitle";
import { WorkspacePanels } from "../components/WorkspacePanels";

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
}

export function WorkspacePage(props: WorkspacePageProps) {
  return (
    <div className="page-shell">
      <section className="content-block split-layout workspace-layout">
        <div>
          <SectionTitle
            eyebrow="Operator layer"
            title="Auth, publishing and moderation"
            body="This screen is built as a serious control surface: login, user context, listing publishing and moderation visibility all share one consistent UI language."
          />
          <MetricStrip
            metrics={[
              { label: "Signed in", value: props.user ? "yes" : "no", tone: "mint" },
              { label: "Role", value: props.user?.role ?? "guest", tone: "sand" },
              { label: "Messages", value: String(props.messages.length), tone: "coral" },
            ]}
          />
          <WorkspacePanels {...props} />
        </div>
        <div>
          <AuthPanel onLogin={props.onLogin} onRegister={props.onRegister} />
        </div>
      </section>
    </div>
  );
}
