import type { Category, Health, Listing } from "../lib/types";
import { HeroPanel } from "../components/HeroPanel";
import { ListingCard } from "../components/ListingCard";
import { MetricStrip } from "../components/MetricStrip";
import { SectionTitle } from "../components/SectionTitle";

interface HomePageProps {
  health: Health | null;
  categories: Category[];
  listings: Listing[];
}

export function HomePage({ health, categories, listings }: HomePageProps) {
  const featuredListings = listings.slice(0, 6);

  return (
    <div className="page-shell">
      <HeroPanel categories={categories} listings={listings} />
      <MetricStrip
        metrics={[
          { label: "Стан сервісу", value: health?.status ?? "loading", tone: "mint" },
          { label: "Категорії", value: String(categories.length), tone: "sand" },
          { label: "Оголошення у вітрині", value: String(listings.length), tone: "coral" },
        ]}
      />
      <section className="content-block spotlight-grid">
        <SectionTitle
          eyebrow="Готово до покупки"
          title="Вітрина, яка допомагає прийняти рішення"
          body="Ми робимо акцент на зрозумілу подачу оголошення: велике фото, чітка категорія, прозора ціна і акуратний статус публікації."
        />
        <div className="trust-panel">
          <div className="trust-card">
            <strong>Модерація перед публікацією</strong>
            <p>Підозрілі або неповні пропозиції можна відсіювати ще до появи у публічному каталозі.</p>
          </div>
          <div className="trust-card">
            <strong>Повідомлення між покупцем і продавцем</strong>
            <p>Контакт починається прямо всередині платформи, без хаотичного переходу в сторонні канали.</p>
          </div>
          <div className="trust-card">
            <strong>Категорії та фільтри без перевантаження</strong>
            <p>Інтерфейс зосереджений на швидкому виборі, а не на десятках другорядних контролів.</p>
          </div>
        </div>
      </section>
      <section className="content-block">
        <SectionTitle
          eyebrow="Популярні зараз"
          title="Оголошення, які виглядають переконливо вже з першого екрану"
          body="Саме така подача найбільше наближує платформу до реального клієнтського продукту: не тільки дані, а й відчуття довіри та цілісності."
        />
        <div className="listing-grid">
          {featuredListings.length ? (
            featuredListings.map((listing) => (
              <ListingCard
                key={listing.id}
                listing={listing}
                category={categories.find((category) => category.id === listing.category_id)}
              />
            ))
          ) : (
            <div className="empty-card hero-empty">
              <strong>Каталог готовий до наповнення</strong>
              <p>
                Платформа вже підключена до API. Додайте категорії й оголошення через кабінет,
                щоб вітрина одразу почала виглядати як реальний маркетплейс.
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
