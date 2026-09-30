import type { ReactNode } from "react";

import { SidebarNav } from "@/components/sidebar-nav";
import { TopBar } from "@/components/top-bar";

export interface DashboardShellProps {
  title: string;
  children: ReactNode;
}

/** Structurally distinct from uis/website: fixed sidebar + topbar admin shell, not a marketing page. */
export function DashboardShell({ title, children }: DashboardShellProps) {
  return (
    <div className="dashboard-shell">
      <SidebarNav />
      <div className="dashboard-content">
        <TopBar title={title} />
        <main className="dashboard-main">{children}</main>
      </div>
    </div>
  );
}
