export default function Topbar({ page }) {
  return <header className="topbar"><div className="breadcrumb"><span>Workspace</span><b>/</b><strong>{page}</strong></div><div className="top-actions"><div className="date-chip"><span>◷</span>{new Date().toLocaleDateString('en-KE', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })}</div><button className="icon-button" title="Notifications">♧<i/></button><div className="header-avatar">JM</div></div></header>;
}
