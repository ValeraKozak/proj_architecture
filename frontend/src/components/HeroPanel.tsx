export function HeroPanel() {
  return (
    <section className="hero-panel">
      <div className="hero-copy">
        <p className="eyebrow">Frontend concept</p>
        <h2>Сильний showcase-шар для платформи оголошень</h2>
        <p>
          Інтерфейс об’єднує каталог, авторизацію, робочий кабінет і модерацію в одному
          цілісному візуальному стилі. Акцент на відчутті реального продукту, а не просто
          навчального CRUD.
        </p>
      </div>
      <div className="hero-art">
        <div className="floating-card warm">
          <span>Listings</span>
          <strong>Modern catalog</strong>
        </div>
        <div className="floating-card mint">
          <span>Moderation</span>
          <strong>Control panel</strong>
        </div>
        <div className="floating-card sand">
          <span>Auth + Dashboard</span>
          <strong>Operator flow</strong>
        </div>
      </div>
    </section>
  );
}
