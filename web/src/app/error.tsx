"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <main className="cg-page">
      <div className="cg-section">
        <article className="cg-panel cg-error-panel">
          <div className="cg-panel-heading">
            <div>
              <span>Something went wrong</span>
            </div>
          </div>
          <p>{error.message || "An unexpected error occurred while loading this page."}</p>
          <div className="cg-hero-actions">
            <button className="cg-button cg-button--dark" type="button" onClick={reset}>
              Try again
            </button>
          </div>
        </article>
      </div>
    </main>
  );
}
