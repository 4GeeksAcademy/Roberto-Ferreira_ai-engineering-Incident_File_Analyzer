"use client";

import { useState } from "react";
import { AnalysisResults } from "./analysis-results";
import { AnalysisUpload } from "./analysis-upload";
import type { AnalysisSummary } from "../types";

export function IncidentAnalysisPage() {
  const [summary, setSummary] = useState<AnalysisSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  return (
    <main className="app-shell">
      <header className="topbar"><a className="brand" href="/"><span className="brand-mark">B</span><span>BRASALAND <small>OPERATIONS</small></span></a><nav aria-label="Main navigation"><a className="nav-link nav-link-active" href="/">Incident analysis</a><a className="nav-link" href="/">Overview</a></nav><div className="user-chip"><span className="avatar">NP</span><span><strong>Nicolás Park</strong><small>Operations</small></span></div></header>
      <div className="page-wrap">
        <div className="page-intro"><div><p className="eyebrow">Operations workspace</p><h1>Incident analysis</h1><p className="intro-copy">Validate and understand the latest incident report before it reaches the operations dashboard.</p></div><div className="status-pill"><span />Ready for upload</div></div>
        <AnalysisUpload onComplete={(next) => { setSummary(next); setError(null); }} onError={setError} loading={loading} setLoading={setLoading} />
        {error && <div className="error-banner" role="alert"><strong>We could not analyze that file</strong><span>{error}</span></div>}
        {summary && <AnalysisResults summary={summary} />}
        {!summary && !error && <div className="empty-state"><span className="empty-icon">▤</span><h2>Your analysis will appear here</h2><p>Upload the incident CSV above to see record quality, categories, statuses, and satisfaction at a glance.</p></div>}
      </div>
      <footer className="footer">Brasaland Digital <span>·</span> Internal operations tool <span>·</span> Data is processed securely and not stored in the browser.</footer>
    </main>
  );
}
