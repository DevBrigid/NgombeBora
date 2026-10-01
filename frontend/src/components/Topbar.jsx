import Icon from './Icon.jsx';

export default function Topbar({ page, onSettings }) {
  return <header className="topbar"><div className="breadcrumb"><span>Workspace</span><b>/</b><strong>{page}</strong></div><div className="top-actions"><div className="date-chip"><span>◷</span>{new Date().toLocaleDateString('en-KE', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })}</div><button className="header-avatar" type="button" aria-label="Open settings" title="Settings" onClick={onSettings}><Icon name="user"/></button></div></header>;
}
