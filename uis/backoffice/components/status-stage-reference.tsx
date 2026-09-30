/**
 * Verbatim from CONTEXT.md ("API and data" section) — the raw API values and the
 * human-readable labels every candidate-facing screen must use instead. This is
 * business logic sourced directly from the briefing, not mocked or invented.
 */
const STATUS_REFERENCE: ReadonlyArray<{ apiValue: string; uiLabel: string }> = [
  { apiValue: "received", uiLabel: "Received" },
  { apiValue: "in_progress", uiLabel: "In progress" },
  { apiValue: "selected", uiLabel: "Selected" },
  { apiValue: "discarded", uiLabel: "Discarded" }
];

const STAGE_REFERENCE: ReadonlyArray<{ apiValue: string; uiLabel: string }> = [
  { apiValue: "pending", uiLabel: "Pending review" },
  { apiValue: "review", uiLabel: "Under review" },
  { apiValue: "personal_interview", uiLabel: "Personal interview" },
  { apiValue: "technical_interview", uiLabel: "Technical interview" },
  { apiValue: "offer_presented", uiLabel: "Offer presented" }
];

export function StatusStageReference() {
  return (
    <section className="panel" aria-labelledby="status-stage-heading">
      <h2 id="status-stage-heading">Status &amp; stage reference</h2>
      <p className="panel-note">
        Raw API values must never be shown to end users — every screen must resolve through this
        mapping, per CONTEXT.md.
      </p>
      <div className="reference-grid">
        <table>
          <caption>Status</caption>
          <thead>
            <tr>
              <th scope="col">API value</th>
              <th scope="col">UI label</th>
            </tr>
          </thead>
          <tbody>
            {STATUS_REFERENCE.map((row) => (
              <tr key={row.apiValue}>
                <td>
                  <code>{row.apiValue}</code>
                </td>
                <td>{row.uiLabel}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <table>
          <caption>Stage</caption>
          <thead>
            <tr>
              <th scope="col">API value</th>
              <th scope="col">UI label</th>
            </tr>
          </thead>
          <tbody>
            {STAGE_REFERENCE.map((row) => (
              <tr key={row.apiValue}>
                <td>
                  <code>{row.apiValue}</code>
                </td>
                <td>{row.uiLabel}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
