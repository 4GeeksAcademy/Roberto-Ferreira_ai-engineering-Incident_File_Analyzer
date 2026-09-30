export interface TopBarProps {
  title: string;
}

export function TopBar({ title }: TopBarProps) {
  return (
    <header className="topbar">
      <h1>{title}</h1>
    </header>
  );
}
