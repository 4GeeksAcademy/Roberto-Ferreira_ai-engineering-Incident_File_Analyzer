export interface StatCardProps {
  value: string;
  label: string;
}

/** Reusable stat tile used to surface a single verified company fact. */
export function StatCard({ value, label }: StatCardProps) {
  return (
    <div className="stat-card">
      <span className="stat-card-value">{value}</span>
      <span className="stat-card-label">{label}</span>
    </div>
  );
}
