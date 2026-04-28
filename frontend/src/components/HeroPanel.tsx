import { Link } from "react-router-dom";

import type { Category, Listing } from "../lib/types";

interface HeroPanelProps {
  categories: Category[];
  listings: Listing[];
}

export function HeroPanel({ categories, listings }: HeroPanelProps) {
  const featuredTitles = listings.slice(0, 3).map((listing) => listing.title);
  const categoryPreview = categories.slice(0, 3).map((category) => category.name).join(" • ");

  return (
    <section className="hero-panel">
      <div className="hero-copy">
        <h2>Знаходьте перевірені пропозиції без зайвого шуму.</h2>
        <p>
          Платформа об&apos;єднує живий каталог, фільтри, повідомлення та модерацію так,
          щоб покупцеві було легко знайти потрібне, а продавцю швидко опублікувати товар.
        </p>
        <div className="hero-actions">
          <Link className="cta-button" to="/catalog">
            Перейти в каталог
          </Link>
          <Link className="ghost-button hero-ghost" to="/workspace">
            Подати оголошення
          </Link>
        </div>
        <div className="hero-search-shell">
          <div className="hero-search-card">
            <span>Популярні категорії</span>
            <strong>{categoryPreview || "Каталог готовий до наповнення"}</strong>
          </div>
          <div className="hero-search-card soft">
            <span>Активна вітрина</span>
            <strong>{listings.length} оголошень доступно зараз</strong>
          </div>
        </div>
      </div>
      <div className="hero-art">
        <div className="floating-card warm hero-story-card">
          <span>Каталог</span>
          <strong>Великі фото, чітка ціна і статуси без хаосу</strong>
          <p>Оголошення виглядають як продуктова вітрина, а не як технічний список записів.</p>
        </div>
        <div className="floating-card mint hero-story-card">
          <span>Довіра</span>
          <strong>Модерація і внутрішні повідомлення</strong>
          <p>Користувач швидше приймає рішення, коли бачить охайну подачу і прозорий шлях до контакту.</p>
        </div>
        <div className="floating-card sand hero-story-card">
          <span>Приклади зараз</span>
          <ul>
            {featuredTitles.length ? (
              featuredTitles.map((title) => <li key={title}>{title}</li>)
            ) : (
              <li>Додайте перші оголошення через кабінет або seed-дані.</li>
            )}
          </ul>
        </div>
      </div>
    </section>
  );
}
