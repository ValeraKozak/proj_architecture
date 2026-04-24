interface MetricStripProps {
  metrics: Array<{ label: string; value: string; tone?: "mint" | "coral" | "sand" }>;
}

export function MetricStrip({ metrics }: MetricStripProps) {
  return (
    <div className="metric-strip">
      {metrics.map((metric) => (
        <article className={`metric-card ${metric.tone ?? "mint"}`} key={metric.label}>
          <span>{metric.label}</span>
          <strong>{metric.value}</strong>
        </article>
      ))}
    </div>
  );
}
