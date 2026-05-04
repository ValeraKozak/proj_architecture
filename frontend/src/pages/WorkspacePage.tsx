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
  onModerateListing: (
    listing_id: number,
    payload: { approved: boolean; rejection_reason?: string | null },
  ) => Promise<void>;
}

export function WorkspacePage(props: WorkspacePageProps) {
  return (
    <div className="page-shell">
      <section className="content-block split-layout workspace-layout">
        <div>
          <SectionTitle
            eyebrow="Кабінет користувача"
            title="Публікуйте, модеруйте і тримайте діалог з клієнтом в одному місці"
            body="Ця зона зібрана навколо реальних задач: увійти без тертя, подати оголошення, побачити чергу модерації й не втратити повідомлення."
          />
          <MetricStrip
            metrics={[
              { label: "Вхід виконано", value: props.user ? "так" : "ні", tone: "mint" },
              { label: "Роль", value: props.user?.role ?? "guest", tone: "sand" },
              { label: "Повідомлення", value: String(props.messages.length), tone: "coral" },
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
