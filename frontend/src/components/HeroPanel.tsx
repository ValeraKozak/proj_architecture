export function HeroPanel() {
  return (
    <section className="hero-panel">
      <div className="hero-copy">
        <p className="eyebrow">Frontend concept</p>
        <h2>Сильний showcase-шар для платформи оголошень</h2>
        <p>
          Інтерфейс об&apos;єднує каталог, авторизацію, робочий кабінет, пошук і модерацію в
          одному цілісному візуальному стилі. Акцент зроблено на відчутті реального
          продукту, а не просто навчального CRUD.
        </p>
      </div>
      <div className="hero-art">
        <div className="floating-card warm">
          <span>Listings</span>
          <strong>Image-first catalog</strong>
        </div>
        <div className="floating-card mint">
          <span>Search</span>
          <strong>Smart filter board</strong>
        </div>
        <div className="floating-card sand">
          <span>Ops</span>
          <strong>Nginx production shell</strong>
        </div>
      </div>
    </section>
  );
}
