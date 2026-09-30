const NAV_LINKS = [
  { href: "#about", label: "About" },
  { href: "#locations", label: "Locations" }
];

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header-inner">
        <span className="brand-mark">Brasaland</span>
        <nav aria-label="Primary">
          <ul className="nav-list">
            {NAV_LINKS.map((link) => (
              <li key={link.href}>
                <a href={link.href}>{link.label}</a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
}
