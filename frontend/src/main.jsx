import React, { useCallback, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import Sidebar from './components/Sidebar.jsx';
import Topbar from './components/Topbar.jsx';
import PageHeader from './components/PageHeader.jsx';
import Toast from './components/Toast.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import HerdPage from './pages/HerdPage.jsx';
import MilkPage from './pages/MilkPage.jsx';
import FinancesPage from './pages/FinancesPage.jsx';
import { api, clearAuthToken, getAuthToken, setAuthToken } from './lib/api.js';
import AuthPage from './pages/AuthPage.jsx';
import SettingsPage from './pages/SettingsPage.jsx';
import { today } from './utils/format.js';
import './styles.css';

function App() {
  const [page, setPage] = useState('Dashboard');
  const [user, setUser] = useState(null);
  const [authReady, setAuthReady] = useState(false);
  const [dashboard, setDashboard] = useState(null);
  const [cows, setCows] = useState([]);
  const [milk, setMilk] = useState([]);
  const [finance, setFinance] = useState({ entries: [], totals: {} });
  const [toast, setToast] = useState('');
  const [query, setQuery] = useState('');
  const [milkDate, setMilkDate] = useState(today());
  const [milkQty, setMilkQty] = useState('');
  const [financeDate, setFinanceDate] = useState(today());
  const [financeType, setFinanceType] = useState('income');
  const [financeCategory, setFinanceCategory] = useState('milk_sales');
  const [financeAmount, setFinanceAmount] = useState('');
  const [financeNote, setFinanceNote] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [cowFlow, setCowFlow] = useState('purchased');
  const [cowForm, setCowForm] = useState({ name: '', breed: '', sex: 'female', mother_id: '', sire_id: '', sire_external: '', date_of_birth: '', birth_weight: '' });

  const refresh = useCallback(async () => {
    try {
      const [summary, herd, milkRecords, ledger] = await Promise.all([
        api('/dashboard'), api('/cows'), api('/milk'), api('/finance'),
      ]);
      setDashboard(summary);
      setCows(herd);
      setMilk(milkRecords);
      setFinance(ledger);
    } catch (error) {
      notify(error.message);
    }
  }, []);

  useEffect(() => {
    let active = true;
    if (!getAuthToken()) { setAuthReady(true); return () => { active = false; }; }
    api('/auth/me').then((currentUser) => { if (active) setUser(currentUser); })
      .catch(() => { clearAuthToken(); if (active) setUser(null); })
      .finally(() => { if (active) setAuthReady(true); });
    return () => { active = false; };
  }, []);

  useEffect(() => {
    const expireSession = () => setUser(null);
    window.addEventListener('ngombebora:session-expired', expireSession);
    return () => window.removeEventListener('ngombebora:session-expired', expireSession);
  }, []);

  useEffect(() => { if (user) refresh(); }, [user, refresh]);
  useEffect(() => {
    if (!user) return;
    const params = new URLSearchParams();
    if (start) params.set('start', start);
    if (end) params.set('end', end);
    if (typeFilter) params.set('type', typeFilter);
    api(`/finance?${params}`).then(setFinance).catch((error) => notify(error.message));
  }, [start, end, typeFilter, user]);

  function notify(message) {
    setToast(message);
    window.setTimeout(() => setToast(''), 3200);
  }

  function handleAuthenticated(result) {
    setAuthToken(result.access_token);
    setUser(result.user);
    setAuthReady(true);
  }

  function handleLogout() {
    clearAuthToken();
    setUser(null);
    setDashboard(null);
    setCows([]);
    setMilk([]);
    setFinance({ entries: [], totals: {} });
  }

  async function saveProfile(payload) {
    const updatedUser = await api('/auth/me', { method: 'PATCH', body: JSON.stringify(payload) });
    setUser(updatedUser);
  }

  async function changePassword(payload) {
    await api('/auth/change-password', { method: 'POST', body: JSON.stringify(payload) });
  }

  async function submitMilk(event) {
    event.preventDefault();
    try {
      await api('/milk', { method: 'POST', body: JSON.stringify({ date: milkDate, quantity: milkQty }) });
      setMilkQty(''); notify('Milk record added'); refresh();
    } catch (error) { notify(error.message); }
  }

  async function submitFinance(event) {
    event.preventDefault();
    try {
      await api('/finance', { method: 'POST', body: JSON.stringify({ date: financeDate, type: financeType, category: financeCategory, amount: financeAmount, note: financeNote }) });
      setFinanceAmount(''); setFinanceNote(''); notify('Ledger entry saved'); refresh();
    } catch (error) { notify(error.message); }
  }

  async function submitCow(event) {
    event.preventDefault();
    const newborn = cowFlow === 'born';
    const payload = newborn
      ? { ...cowForm, mother_id: Number(cowForm.mother_id), sire_id: cowForm.sire_id ? Number(cowForm.sire_id) : null }
      : cowForm;
    try {
      const cow = await api(`/cows/${newborn ? 'newborn' : 'purchased'}`, { method: 'POST', body: JSON.stringify(payload) });
      notify(`${cow.name} registered · ${cow.serial_number}`);
      setCowForm({ ...cowForm, name: '', birth_weight: '', sire_external: '', sire_id: '' });
      refresh();
    } catch (error) { notify(error.message); }
  }

  async function setCowStatus(cow, status) {
    try {
      await api(`/cows/${cow.id}/status`, { method: 'PATCH', body: JSON.stringify({ status }) });
      notify(`${cow.name} marked ${status}`); refresh();
    } catch (error) { notify(error.message); }
  }

  const filteredCows = cows.filter((cow) => [cow.name, cow.serial_number, cow.breed].join(' ').toLowerCase().includes(query.toLowerCase()));
  const pageProps = {
    dashboard, setPage, setCowFlow,
    cowFlow, cowForm, setCowForm, cows, submitCow, query, setQuery, filteredCows, setStatus: setCowStatus,
    milkDate, setMilkDate, milkQty, setMilkQty, submitMilk, milk,
    financeDate, setFinanceDate, financeType, setFinanceType, financeCategory, setFinanceCategory,
    financeAmount, setFinanceAmount, financeNote, setFinanceNote, start, setStart, end, setEnd,
    typeFilter, setTypeFilter, submitFinance, finance,
  };
  const pages = {
    Dashboard: <DashboardPage {...pageProps}/>,
    Herd: <HerdPage {...pageProps}/>,
    'Milk log': <MilkPage {...pageProps}/>,
    Finances: <FinancesPage {...pageProps}/>,
    Settings: <SettingsPage user={user} onSaveProfile={saveProfile} onChangePassword={changePassword}/>,
  };

  if (!authReady) return <div className="auth-loading">Loading your farm…</div>;
  if (!user) return <AuthPage onAuthenticated={handleAuthenticated}/>;

  return <div className="app-shell">
    <Sidebar page={page} setPage={setPage} activeCows={dashboard?.active_cows} onLogout={handleLogout}/>
    <main className="main">
      <Topbar page={page} onSettings={() => setPage('Settings')}/>
      <div className="content">
        <PageHeader page={page} user={user}/>
        {pages[page]}
        <footer>NgombeBora <span>·</span> Good farming, better living <span className="footer-right">Your farm data stays yours.</span></footer>
      </div>
    </main>
    <Toast message={toast}/>
  </div>;
}

createRoot(document.getElementById('root')).render(<React.StrictMode><App/></React.StrictMode>);
