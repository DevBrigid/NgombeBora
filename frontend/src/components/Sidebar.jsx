import Icon from './Icon.jsx';

const navigation = [['Dashboard', 'home'], ['Herd', 'cows'], ['Milk log', 'milk'], ['Finances', 'ledger'], ['Settings', 'settings']];

export default function Sidebar({ page, setPage, activeCows, onLogout }) {
  return <aside className="sidebar">
    <div className="brand"><div className="brand-mark"><Icon name="cow"/></div><div><b>ngombebora</b><small>FARM MANAGEMENT</small></div></div>
    <p className="nav-label">WORKSPACE</p>
    <nav>{navigation.map(([label, icon]) => <button className={page === label ? 'nav-item active' : 'nav-item'} onClick={() => setPage(label)} key={label}><Icon name={icon}/><span>{label}</span>{label === 'Herd' && <i>{activeCows ?? '–'}</i>}</button>)}</nav>
    <div className="sidebar-bottom">
      <button className="sidebar-logout" type="button" onClick={onLogout}><Icon name="logout"/><span>Sign out</span></button>
    </div>
  </aside>;
}
