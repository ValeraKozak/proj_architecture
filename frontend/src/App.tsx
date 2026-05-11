import { useEffect, useMemo, useState } from "react";
import { Route, Routes, useLocation, useNavigate } from "react-router-dom";

import { Header } from "./components/Header";
import { APIError, api } from "./lib/api";
import type { Category, Health, Listing, Message, User } from "./lib/types";
import { CatalogPage } from "./pages/CatalogPage";
import { ErrorPage } from "./pages/ErrorPage";
import { HomePage } from "./pages/HomePage";
import { ListingDetailPage } from "./pages/ListingDetailPage";
import { WorkspacePage } from "./pages/WorkspacePage";

const TOKEN_KEY = "bulletin-board-token";

function resolvePageError(error: unknown): number | null {
  if (!(error instanceof APIError)) {
    return null;
  }
  if (error.status >= 500) {
    return 500;
  }
  if (error.status === 400) {
    return 400;
  }
  return null;
}

export function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const [health, setHealth] = useState<Health | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [listings, setListings] = useState<Listing[]>([]);
  const [user, setUser] = useState<User | null>(null);
  const [myListings, setMyListings] = useState<Listing[]>([]);
  const [pendingListings, setPendingListings] = useState<Listing[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [token, setToken] = useState<string>(() => window.localStorage.getItem(TOKEN_KEY) ?? "");

  async function refreshPublicData() {
    const [healthData, categoryData, listingData] = await Promise.all([
      api.health(),
      api.categories(),
      api.listings(),
    ]);
    setHealth(healthData);
    setCategories(categoryData);
    setListings(listingData);
  }

  async function refreshPrivateData(activeToken: string) {
    const profile = await api.me(activeToken);
    setUser(profile);

    const [owned, inbox] = await Promise.all([api.myListings(activeToken), api.messages(activeToken)]);
    setMyListings(owned);
    setMessages(inbox);

    if (profile.role === "moderator" || profile.role === "admin") {
      setPendingListings(await api.pendingListings(activeToken));
    } else {
      setPendingListings([]);
    }
  }

  useEffect(() => {
    refreshPublicData().catch((error) => {
      console.error(error);
      const code = resolvePageError(error);
      if (code) {
        navigate(`/errors/${code}`, { replace: true });
      }
    });
  }, [navigate]);

  useEffect(() => {
    if (!token) {
      setUser(null);
      setMyListings([]);
      setPendingListings([]);
      setMessages([]);
      return;
    }

    refreshPrivateData(token).catch((error) => {
      console.error(error);

      if (error instanceof APIError && (error.status === 401 || error.status === 403)) {
        window.localStorage.removeItem(TOKEN_KEY);
        setToken("");
        return;
      }

      const code = resolvePageError(error);
      if (code) {
        navigate(`/errors/${code}`, { replace: true });
      }
    });
  }, [navigate, token]);

  async function handleLogin(email: string, password: string) {
    const result = await api.login(email, password);
    window.localStorage.setItem(TOKEN_KEY, result.access_token);
    setToken(result.access_token);
  }

  async function handleRegister(email: string, fullName: string, password: string) {
    await api.register(email, fullName, password);
    await handleLogin(email, password);
  }

  function handleLogout() {
    window.localStorage.removeItem(TOKEN_KEY);
    setToken("");
  }

  async function handleCreateListing(payload: {
    title: string;
    description: string;
    price: number;
    category_id: number;
    image_urls: string[];
  }) {
    if (!token) {
      throw new Error("Login required");
    }
    await api.createListing(token, payload);
    await Promise.all([refreshPublicData(), refreshPrivateData(token)]);
  }

  async function handleUploadImages(files: File[]) {
    if (!token) {
      throw new Error("Login required");
    }
    return api.uploadImages(token, files);
  }

  async function handleCreateCategory(payload: { name: string; description: string }) {
    if (!token) {
      throw new Error("Login required");
    }
    await api.createCategory(token, payload);
    await refreshPublicData();
    await refreshPrivateData(token);
  }

  async function handleModerateListing(
    listing_id: number,
    payload: { approved: boolean; rejection_reason?: string | null },
  ) {
    if (!token) {
      throw new Error("Login required");
    }
    await api.moderateListing(token, listing_id, payload);
    await Promise.all([refreshPublicData(), refreshPrivateData(token)]);
  }

  async function handleSendMessage(payload: {
    listing_id: number;
    recipient_id: number;
    body: string;
  }) {
    if (!token) {
      throw new Error("Login required");
    }
    await api.sendMessage(token, payload);
    await refreshPrivateData(token);
  }

  const isAuthenticated = useMemo(() => Boolean(token && user), [token, user]);
  const isErrorRoute = location.pathname.startsWith("/errors/");

  return (
    <div className={`app-shell${isErrorRoute ? " app-shell--error" : ""}`}>
      {isErrorRoute ? null : (
        <Header
          isAuthenticated={isAuthenticated}
          onLogout={handleLogout}
          userName={user?.full_name}
        />
      )}
      <main>
        <Routes>
          <Route path="/" element={<HomePage health={health} categories={categories} listings={listings} />} />
          <Route path="/catalog" element={<CatalogPage categories={categories} />} />
          <Route
            path="/catalog/:listingId"
            element={
              <ListingDetailPage
                categories={categories}
                listings={listings}
                messages={messages}
                onSendMessage={handleSendMessage}
                token={token}
                user={user}
              />
            }
          />
          <Route
            path="/workspace"
            element={
              <WorkspacePage
                categories={categories}
                messages={messages}
                myListings={myListings}
                onCreateCategory={handleCreateCategory}
                onCreateListing={handleCreateListing}
                onLogin={handleLogin}
                onModerateListing={handleModerateListing}
                onRegister={handleRegister}
                onSendMessage={handleSendMessage}
                pendingListings={pendingListings}
                user={user}
              />
            }
          />
          <Route path="/errors/:code" element={<ErrorPage />} />
          <Route path="*" element={<ErrorPage code={404} />} />
        </Routes>
      </main>
    </div>
  );
}
