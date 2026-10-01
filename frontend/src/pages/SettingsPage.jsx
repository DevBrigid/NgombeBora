import { useEffect, useState } from 'react';
import Icon from '../components/Icon.jsx';

export default function SettingsPage({ user, onSaveProfile, onChangePassword }) {
  const [profile, setProfile] = useState({ name: user.name, email: user.email });
  const [password, setPassword] = useState({ current_password: '', new_password: '', confirm_password: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [saving, setSaving] = useState('');

  useEffect(() => setProfile({ name: user.name, email: user.email }), [user.name, user.email]);

  async function saveProfile(event) {
    event.preventDefault(); setError(''); setMessage(''); setSaving('profile');
    try { await onSaveProfile(profile); setMessage('Your account details are up to date.'); }
    catch (requestError) { setError(requestError.message); }
    finally { setSaving(''); }
  }

  async function savePassword(event) {
    event.preventDefault(); setError(''); setMessage('');
    if (password.new_password !== password.confirm_password) { setError('The new passwords do not match.'); return; }
    setSaving('password');
    try {
      await onChangePassword({ current_password: password.current_password, new_password: password.new_password });
      setPassword({ current_password: '', new_password: '', confirm_password: '' });
      setMessage('Your password has been changed.');
    } catch (requestError) { setError(requestError.message); }
    finally { setSaving(''); }
  }

  return <div className="settings-page">
    <section className="panel settings-panel">
      <div className="panel-header"><div><div className="panel-eyebrow">ACCOUNT</div><h2>Profile details</h2><p>Update the name and email associated with your account.</p></div><span className="metric-icon green"><Icon name="user"/></span></div>
      <form className="settings-form" onSubmit={saveProfile}>
        <label>Full name<input autoComplete="name" required maxLength="120" value={profile.name} onChange={event => setProfile({ ...profile, name: event.target.value })}/></label>
        <label>Email address<input autoComplete="email" required type="email" maxLength="254" value={profile.email} onChange={event => setProfile({ ...profile, email: event.target.value })}/></label>
        <button className="button primary" disabled={saving !== ''}>{saving === 'profile' ? 'Saving…' : 'Save profile'}</button>
      </form>
    </section>
    <section className="panel settings-panel">
      <div className="panel-header"><div><div className="panel-eyebrow">SECURITY</div><h2>Change password</h2><p>Choose a password with at least 8 characters.</p></div><span className="metric-icon cream"><Icon name="lock"/></span></div>
      <form className="settings-form" onSubmit={savePassword}>
        <label>Current password<input required type="password" autoComplete="current-password" value={password.current_password} onChange={event => setPassword({ ...password, current_password: event.target.value })}/></label>
        <label>New password<input required minLength="8" maxLength="128" type="password" autoComplete="new-password" value={password.new_password} onChange={event => setPassword({ ...password, new_password: event.target.value })}/></label>
        <label>Confirm new password<input required minLength="8" maxLength="128" type="password" autoComplete="new-password" value={password.confirm_password} onChange={event => setPassword({ ...password, confirm_password: event.target.value })}/></label>
        <button className="button primary" disabled={saving !== ''}>{saving === 'password' ? 'Updating…' : 'Update password'}</button>
      </form>
    </section>
    {(error || message) && <div className={error ? 'settings-message error' : 'settings-message'} role={error ? 'alert' : 'status'}>{error || message}</div>}
  </div>;
}
