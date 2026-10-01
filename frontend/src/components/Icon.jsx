const paths = {
  home: 'M3 10.8 12 3l9 7.8v9.7a.5.5 0 0 1-.5.5h-5.8v-6.4H9.3V21H3.5a.5.5 0 0 1-.5-.5z',
  cows: 'M4 9 2 6v-2l5 2h10l5-2v2l-2 3v8h-3v3h-3v-3h-4v3H7v-3H4z M8 11h.01M16 11h.01',
  milk: 'M8 3h8l1 4 2 2v12H5V9l2-2z M7 7h10 M8 13h8',
  ledger: 'M6 3h12v18l-2-1-2 1-2-1-2 1-2-1-2 1z M9 8h6m-6 4h6m-6 4h4',
  plus: 'M12 5v14M5 12h14',
  search: 'm20 20-4.5-4.5 M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0',
  arrow: 'M5 12h14m-6-6 6 6-6 6',
  cow: 'M3 8 1 5v-2l5 2h12l5-2v2l-2 3v9h-4v3h-3v-3h-4v3H7v-3H3z',
  user: 'M20 21a8 8 0 0 0-16 0 M12 13a5 5 0 1 0 0-10 5 5 0 0 0 0 10z',
  logout: 'M10 17l5-5-5-5 M15 12H3 M12 3h6a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-6',
  lock: 'M5 11h14v10H5z M8 11V7a4 4 0 1 1 8 0v4',
  settings: 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-1.7 2.9-.2-.1a1.7 1.7 0 0 0-1.8.1l-.2.1h-3.4l-.1-.2a1.7 1.7 0 0 0-1.6-1l-.2.1-3-1.7.1-.2a1.7 1.7 0 0 0-.1-1.8l-.1-.2v-3.4l.2-.1a1.7 1.7 0 0 0 1-1.6l-.1-.2 1.7-3 .2.1a1.7 1.7 0 0 0 1.8-.1l.2-.1h3.4l.1.2a1.7 1.7 0 0 0 1.6 1l.2-.1 3 1.7-.1.2a1.7 1.7 0 0 0 .1 1.8l.1.2v3.4z',
};

export default function Icon({ name }) {
  return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={paths[name] || paths.cow}/></svg>;
}
