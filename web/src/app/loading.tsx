export default function Loading() {
  return (
    <main className="cg-page">
      <div className="cg-section">
        <div className="cg-card-grid cg-card-grid--three" aria-busy="true" aria-label="Loading content">
          {Array.from({ length: 3 }).map((_, i) => (
            <article key={i} className="cg-card cg-card--skeleton">
              <div className="cg-card-topline">
                <span className="cg-skeleton-text cg-skeleton-text--badge" />
                <span className="cg-skeleton-text cg-skeleton-text--short" />
              </div>
              <span className="cg-skeleton-text cg-skeleton-text--heading" />
              <span className="cg-skeleton-text cg-skeleton-text--body" />
              <span className="cg-skeleton-text cg-skeleton-text--body" />
            </article>
          ))}
        </div>
      </div>
    </main>
  );
}
