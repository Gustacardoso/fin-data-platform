const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface Financial {
  id: number;
  source: string;
  description: string;
  amount: number;
  date: string;
}

export interface Summary {
  income: number;
  expenses: number;
  balance: number;
  count: number;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`Erro ${res.status} em ${path}`);
  return res.json() as Promise<T>;
}

export const fetchSummary = () => get<Summary>("/financial/summary");
export const fetchFinancial = (limit: number, offset: number) =>
  get<Financial[]>(`/financial?limit=${limit}&offset=${offset}`);
