import { ActiveSearchCard } from "@/components/active-search-card";
import { DashboardShell } from "@/components/dashboard-shell";
import { StatusStageReference } from "@/components/status-stage-reference";

export default function HomePage() {
  return (
    <DashboardShell title="Recruiting overview">
      <ActiveSearchCard />
      <StatusStageReference />
    </DashboardShell>
  );
}
