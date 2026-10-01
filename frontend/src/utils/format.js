export const money = (amount) => `KES ${Number(amount || 0).toLocaleString('en-KE', { maximumFractionDigits: 0 })}`;
export const today = () => new Date().toISOString().slice(0, 10);
