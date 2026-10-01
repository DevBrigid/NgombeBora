import Icon from './Icon.jsx';

const copy = {
  Dashboard: ['Good morning, farmer', "Here's what's happening on your farm today."],
  Herd: ['Your herd', 'Keep track of every animal, from newborn calves to mature cows.'],
  'Milk log': ['Milk production', 'A clear view of your herd’s daily milk production.'],
  Finances: ['Financial ledger', 'Keep your income and expenses organized in one place.'],
};

export default function PageHeader({ page }) {
  const [title, description] = copy[page];
  return <div className="page-heading"><div><div className="eyebrow"><span className="eyebrow-dot"/> YOUR FARM AT A GLANCE</div><h1>{title}<span className="wave">✳</span></h1><p>{description}</p></div>{page === 'Herd' && <button className="button primary" onClick={() => document.getElementById('cow-registration')?.scrollIntoView({ behavior: 'smooth' })}><Icon name="plus"/> Register cow</button>}</div>;
}
