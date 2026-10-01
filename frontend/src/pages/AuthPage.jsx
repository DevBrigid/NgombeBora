import { useState } from 'react';
import Icon from '../components/Icon.jsx';
import { api } from '../lib/api.js';

export default function AuthPage({ onAuthenticated }) {
  const [mode, setMode] = useState('login');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const isSignup = mode === 'signup';

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      const result = await api(`/auth/${isSignup ? 'register' : 'login'}`, {
        method: 'POST',
        body: JSON.stringify({ name, email, password }),
      });
      onAuthenticated(result);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return <main className="auth-screen">
    <section className="auth-story">
      <div className="auth-brand"><span className="brand-mark"><Icon name="cow"/></span><span><b>ngombebora</b><small>FARM MANAGEMENT</small></span></div>
      <div className="auth-story-copy"><span className="auth-eyebrow"><i/> YOUR FARM, IN GOOD HANDS</span><h1>Good farming.<br/><em>Better living.</em></h1><p>One clear view of your cattle, the care they need, and the work that keeps your herd thriving.</p><div className="auth-benefits"><div><span>01</span><b>Every animal has a story</b></div><div><span>02</span><b>Every litre, accounted for</b></div><div><span>03</span><b>Every shilling in view</b></div></div></div>
      <div className="auth-story-footer"><span>✳</span> Built for the people who grow our future.</div>
      <div className="auth-orbit orbit-one"/><div className="auth-orbit orbit-two"/>
    </section>
    <section className="auth-panel-wrap"><div className="auth-panel">
      <div className="auth-mobile-brand"><span className="brand-mark"><Icon name="cow"/></span><b>ngombebora</b></div>
      <div className="auth-panel-kicker">WELCOME TO YOUR FARM</div>
      <h2>{isSignup ? 'Create your account' : 'Welcome back'}</h2>
      <p className="auth-intro">{isSignup ? 'Set up your account to manage your farm in one place.' : 'Sign in to pick up where you left off.'}</p>
      <form onSubmit={handleSubmit} className="auth-form">
        {isSignup && <label>Your name<input autoComplete="name" required maxLength="120" value={name} onChange={event => setName(event.target.value)} placeholder="e.g. Jane Wanjiku"/></label>}
        <label>Email address<input autoComplete="email" type="email" required maxLength="254" value={email} onChange={event => setEmail(event.target.value)} placeholder="you@example.com"/></label>
        <label>Password<span className="auth-password-wrap"><input autoComplete={isSignup ? 'new-password' : 'current-password'} type={showPassword ? 'text' : 'password'} required minLength={isSignup ? 8 : undefined} maxLength="128" value={password} onChange={event => setPassword(event.target.value)} placeholder={isSignup ? 'At least 8 characters' : 'Enter your password'}/><button type="button" className="password-toggle" onClick={() => setShowPassword(value => !value)}>{showPassword ? 'Hide' : 'Show'}</button></span></label>
        {error && <div className="auth-error" role="alert">{error}</div>}
        <button className="button primary auth-submit" type="submit" disabled={loading}>{loading ? 'Please wait…' : isSignup ? 'Create account' : 'Sign in'}<Icon name="arrow"/></button>
      </form>
      <div className="auth-switch">{isSignup ? 'Already have an account?' : 'New to NgombeBora?'} <button onClick={() => { setError(''); setMode(isSignup ? 'login' : 'signup'); }}>{isSignup ? 'Sign in' : 'Create an account'}</button></div>
      <div className="auth-secure"><span>◈</span> Your farm information is private and secure</div>
    </div></section>
  </main>;
}
