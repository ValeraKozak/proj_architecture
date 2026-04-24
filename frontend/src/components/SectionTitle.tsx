interface SectionTitleProps {
  eyebrow: string;
  title: string;
  body: string;
}

export function SectionTitle({ eyebrow, title, body }: SectionTitleProps) {
  return (
    <div className="section-title">
      <p className="eyebrow">{eyebrow}</p>
      <h3>{title}</h3>
      <p>{body}</p>
    </div>
  );
}
