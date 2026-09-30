import type { AnalysisSummary, Breakdown } from "../types";
import { resultsExportUrl } from "../lib/api-client";

const CATEGORY_LABELS: Record<string, string> = {
  CUSTOMER_COMPLAINT: "Customer complaint",
  EQUIPMENT: "Equipment",
  SUPPLY: "Supply",
  FOOD_QUALITY: "Food quality",
  STAFF: "Staff",
};

const STATUS_LABELS: Record<string, string> = {
  OPEN: "Open",
  CLOSED: "Closed",
  DISCARDED: "Discarded",
};

const REASON_LABELS: Record<string, string> = {
  missing_or_invalid_location_id: "Missing or invalid location",
  missing_or_invalid_category: "Missing or invalid category",
  empty_or_too_short_description: "Empty or too-short description",
  missing_reporter_id: "Missing reporter",
  closed_without_satisfaction_score: "Closed case without satisfaction score",
  satisfaction_score_out_of_range: "Satisfaction score out of range",
};

function percentage(value: number, total: number) {
  return total ? `${((value / total) * 100).toFixed(1)}%` : "0.0%";
}

function BreakdownList({ items, total, labels }: { items: Breakdown; total: number; labels: Record<string, string> }) {
  return (
    <div className="breakdown-list">
      {Object.entries(items).map(([key, value]) => (
        <div className="breakdown-row" key={key}>
          <div className="breakdown-label"><span>{labels[key] ?? key}</span><strong>{value}</strong></div>
          <div className="progress-track"><span style={{ width: percentage(value, total) }} /></div>
          <small>{percentage(value, total)}</small>
        </div>
      ))}
    </div>
  );
}

export function AnalysisResults({ summary }: { summary: AnalysisSummary }) {
  return (
    <section className="results" aria-labelledby="results-title">
      <div className="results-heading">
        <div>
          <p className="eyebrow">Latest analysis</p>
          <h2 id="results-title">Incident report overview</h2>
          <p className="muted">Metrics are based on valid records unless noted otherwise.</p>
        </div>
        <a className="button button-primary" href={resultsExportUrl()} download="results.csv">Download CSV <span aria-hidden="true">↓</span></a>
      </div>

      <div className="metric-grid">
        <article className="metric-card metric-card-total"><span>Total records</span><strong>{summary.total_records}</strong><small>Records received</small></article>
        <article className="metric-card metric-card-valid"><span>Valid records</span><strong>{summary.valid_records}</strong><small>{percentage(summary.valid_records, summary.total_records)} of total</small></article>
        <article className="metric-card metric-card-invalid"><span>Invalid records</span><strong>{summary.invalid_records}</strong><small>{percentage(summary.invalid_records, summary.total_records)} need attention</small></article>
        <article className="metric-card metric-card-satisfaction"><span>Average satisfaction</span><strong>{summary.average_satisfaction?.toFixed(2) ?? "—"}<small> / 5</small></strong><small>{summary.satisfaction_sample_size} scored closed cases</small></article>
      </div>

      {summary.invalid_records > 0 && (
        <div className="notice" role="status">
          <div className="notice-icon">!</div>
          <div><strong>{summary.invalid_records} records need attention</strong><p>These records were excluded from the valid breakdowns. Review the detected reasons below.</p><ul>{Object.entries(summary.invalid_by_reason).map(([reason, count]) => <li key={reason}><span>{REASON_LABELS[reason] ?? reason}</span><strong>{count}</strong></li>)}</ul></div>
        </div>
      )}

      <div className="panel-grid">
        <article className="panel"><div className="panel-title"><div><p className="eyebrow">Valid records</p><h3>By category</h3></div><span className="panel-total">{summary.valid_records}</span></div><BreakdownList items={summary.category_breakdown} total={summary.valid_records} labels={CATEGORY_LABELS} /></article>
        <article className="panel"><div className="panel-title"><div><p className="eyebrow">Record state</p><h3>By status</h3></div><span className="panel-total">{summary.valid_records}</span></div><BreakdownList items={summary.status_breakdown} total={summary.valid_records} labels={STATUS_LABELS} /></article>
      </div>

      <article className="panel satisfaction-panel"><div className="panel-title"><div><p className="eyebrow">Closed cases</p><h3>Satisfaction index</h3></div><div className="score-summary"><strong>{summary.average_satisfaction?.toFixed(2) ?? "—"}</strong><span>/ 5.00 average</span></div></div><div className="score-grid">{Object.entries(summary.satisfaction_distribution).map(([score, count]) => <div className="score-item" key={score}><div className="score-number">{score}</div><strong>{count}</strong><span>{Number(score) === 1 ? "Very dissatisfied" : Number(score) === 5 ? "Very satisfied" : Number(score) === 3 ? "Neutral" : Number(score) === 2 ? "Dissatisfied" : "Satisfied"}</span></div>)}</div></article>
    </section>
  );
}
