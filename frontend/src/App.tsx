import { useEffect, useMemo, useState } from "react";
import { Route, Routes } from "react-router-dom";

import { Header } from "./components/Header";
import { api } from "./lib/api";
import type { Category, Health, Listing, Message, User } from "./lib/types";
import { CatalogPage } from "./pages/CatalogPage";
import { HomePage } from "./pages/HomePage";
import { WorkspacePage } from "./pages/WorkspacePage";

const TOKEN_KEY = "bulletin-board-token";

export function App() {
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
    refreshPublicData().catch(console.error);
  }, []);

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
      window.localStorage.removeItem(TOKEN_KEY);
      setToken("");
    });
  }, [token]);

  async function handleLogin(email: string, password: string) {
    const result = await api.login(email, password);
    window.localStorage.setItem(TOKEN_KEY, result.access_token);
    setToken(result.access_token);
  }

  async function handleRegister(email: string, fullName: string, password: string) {
    await api.register(email, fullName, password);
    await handleLogin(email, password);
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

  async function handleCreateCategory(payload: { name: string; description: string }) {
    if (!token) {
      throw new Error("Login required");
    }
    await api.createCategory(token, payload);
    await refreshPublicData();
    await refreshPrivateData(token);
  }

  const isAuthenticated = useMemo(() => Boolean(token && user), [token, user]);

  return (
    <div className="app-shell">
      <Header isAuthenticated={isAuthenticated} userName={user?.full_name} />
      <main>
        <Routes>
          <Route path="/" element={<HomePage health={health} categories={categories} listings={listings} />} />
          <Route path="/catalog" element={<CatalogPage categories={categories} />} />
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
                onRegister={handleRegister}
                pendingListings={pendingListings}
                user={user}
              />
            }
          />
        </Routes>
      </main>
    </div>
  );
}
