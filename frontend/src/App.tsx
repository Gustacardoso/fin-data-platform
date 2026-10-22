import { useCallback, useEffect, useState } from "react";
import { fetchFinancial, fetchSummary, type Financial, type Summary } from "./api";
import { AmountChart, FinancialTable, SummaryCards } from "./components";

const PAGE_SIZE = 10;

export default function App() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [rows, setRows] = useState<Financial[]>([]);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [s, r] = await Promise.all([
        fetchSummary(),
        fetchFinancial(PAGE_SIZE, page * PAGE_SIZE),
      ]);
      setSummary(s);
      setRows(r);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Falha ao carregar dados");
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <main className="container">
      <header className="top">
        <h1>Fin Data</h1>
        <button onClick={load} disabled={loading}>{loading ? "Carregando..." : "Atualizar"}</button>
      </header>

      {error && <div className="error">{error}. A API está rodando em localhost:8000?</div>}
      {summary && <SummaryCards summary={summary} />}
      <AmountChart rows={rows} />
      <FinancialTable rows={rows} page={page} pageSize={PAGE_SIZE} onPage={setPage} />
    </main>
  );
}
