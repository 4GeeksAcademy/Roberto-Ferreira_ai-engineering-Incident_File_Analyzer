const NAV_ITEMS = [
  { label: "Dashboard", href: "#" },
  { label: "Candidates", href: "#" },
  { label: "Notes", href: "#" }
];

export function SidebarNav() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">Brasaland Backoffice</div>
      <nav aria-label="Backoffice">
        <ul className="sidebar-nav-list">
          {NAV_ITEMS.map((item) => (
            <li key={item.label}>
              <a href={item.href}>{item.label}</a>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
