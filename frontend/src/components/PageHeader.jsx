import Icon from './Icon.jsx';

const copy = {
  Dashboard: ['Welcome back', "Here's what's happening with your herd today."],
  Herd: ['Your herd', 'Keep track of every animal, from newborn calves to mature cows.'],
  'Milk log': ['Milk production', 'A clear view of your herd’s daily milk production.'],
  Finances: ['Financial ledger', 'Keep your income and expenses organized in one place.'],
  Settings: ['Account settings', 'Manage your profile details and password.'],
};

export default function PageHeader({ page, user }) {
  const [defaultTitle, description] = copy[page];
  const firstName = user?.name?.trim().split(/\s+/)[0];
  const title = page === 'Dashboard' && firstName ? `Welcome back, ${firstName}` : defaultTitle;
  return <div className="page-heading"><div><div className="eyebrow"><span className="eyebrow-dot"/> YOUR FARM AT A GLANCE</div><h1>{title}<span className="wave">✳</span></h1><p>{description}</p></div>{page === 'Herd' && <button className="button primary" onClick={() => document.getElementById('cow-registration')?.scrollIntoView({ behavior: 'smooth' })}><Icon name="plus"/> Register cow</button>}</div>;
}
