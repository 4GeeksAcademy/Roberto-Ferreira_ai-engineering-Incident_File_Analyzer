/**
 * Verbatim from CONTEXT.md ("Context of the active search") — the current hiring
 * requisition this backoffice exists to support. No mock/live-API data involved.
 */
const ACTIVE_SEARCH = {
  position: "Executive Assistant",
  company: "Brasaland",
  location: "Corporate headquarters, Medellín",
  profile: "Executive support experience, calendar and travel management, professional English"
} as const;

export function ActiveSearchCard() {
  return (
    <section className="panel" aria-labelledby="active-search-heading">
      <h2 id="active-search-heading">Active search</h2>
      <dl className="definition-list">
        <dt>Position</dt>
        <dd>{ACTIVE_SEARCH.position}</dd>

        <dt>Company</dt>
        <dd>{ACTIVE_SEARCH.company}</dd>

        <dt>Location</dt>
        <dd>{ACTIVE_SEARCH.location}</dd>

        <dt>Profile</dt>
        <dd>{ACTIVE_SEARCH.profile}</dd>
      </dl>
    </section>
  );
}
