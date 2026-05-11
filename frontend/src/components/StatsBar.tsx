interface StatsBarProps {
  metrics: Array<{ label: string; value: string; description: string }>;
}

export function StatsBar({ metrics }: StatsBarProps) {
  return (
    <section className="stats-bar" id="stats">
      {metrics.map((metric) => (
        <article className="stats-bar__item" key={metric.label}>
          <div className="stats-bar__icon" aria-hidden="true" />
          <div>
            <strong>{metric.value}</strong>
            <span>{metric.label}</span>
            <small>{metric.description}</small>
          </div>
        </article>
      ))}
    </section>
  );
}
