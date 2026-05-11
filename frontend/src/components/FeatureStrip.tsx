import { featureStripItems } from "../lib/ui-demo";

export function FeatureStrip() {
  return (
    <section className="feature-strip" id="resources">
      {featureStripItems.map((item) => (
        <article className="feature-strip__item" key={item.title}>
          <div className="feature-strip__icon" aria-hidden="true" />
          <div>
            <strong>{item.title}</strong>
            <p>{item.body}</p>
          </div>
        </article>
      ))}
    </section>
  );
}
