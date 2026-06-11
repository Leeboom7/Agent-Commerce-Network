import Link from "next/link";

export default function NotFound() {
  return (
    <main className="cg-page">
      <div className="cg-section">
        <article className="cg-panel cg-error-panel">
          <div className="cg-panel-heading">
            <div>
              <span>Page not found</span>
            </div>
          </div>
          <p>The page you are looking for doesn&apos;t exist or has been moved.</p>
          <div className="cg-hero-actions">
            <Link className="cg-button cg-button--dark" href="/">
              Back to Home
            </Link>
            <Link className="cg-button cg-button--light" href="/console">
              Open Console
            </Link>
          </div>
        </article>
      </div>
    </main>
  );
}
