import Icon from './Icon.jsx';

const navigation = [['Dashboard', 'home'], ['Herd', 'cows'], ['Milk log', 'milk'], ['Finances', 'ledger']];

export default function Sidebar({ page, setPage, activeCows }) {
  return <aside className="sidebar">
    <div className="brand"><div className="brand-mark"><Icon name="cow"/></div><div><b>ngombebora</b><small>FARM MANAGEMENT</small></div></div>
    <div className="farm-card"><div className="farm-avatar">MK</div><div><strong>Mavuno Farm</strong><span>Kiambu County, Kenya</span></div><span className="chevron">⌄</span></div>
    <p className="nav-label">WORKSPACE</p>
    <nav>{navigation.map(([label, icon]) => <button className={page === label ? 'nav-item active' : 'nav-item'} onClick={() => setPage(label)} key={label}><Icon name={icon}/><span>{label}</span>{label === 'Herd' && <i>{activeCows ?? '–'}</i>}</button>)}</nav>
    <div className="sidebar-bottom"><div className="weather"><span className="sun">☀</span><div><b>Farm overview</b><span>All systems in order</span></div><span className="online-dot"/></div><div className="profile"><div className="profile-pic">JM</div><div><b>James Mwangi</b><span>Farm owner</span></div><span className="more">···</span></div></div>
  </aside>;
}
