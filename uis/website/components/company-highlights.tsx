import { StatCard } from "@/components/stat-card";

const COMPANY_STATS = [
  { value: "14", label: "Locations" },
  { value: "2", label: "Countries — Colombia & Florida (USA)" },
  { value: "Medellín", label: "Corporate headquarters" }
];

export function CompanyHighlights() {
  return (
    <section id="about" className="company-highlights">
      <h2>Who we are</h2>
      <p>
        Brasaland is a grilled food restaurant chain with locations across Colombia and Florida.
        Our corporate headquarters is based in Medellín, and our teams work every day to bring
        consistent, freshly grilled meals to every location we serve.
      </p>
      <div className="stat-grid">
        {COMPANY_STATS.map((stat) => (
          <StatCard key={stat.label} value={stat.value} label={stat.label} />
        ))}
      </div>
    </section>
  );
}
