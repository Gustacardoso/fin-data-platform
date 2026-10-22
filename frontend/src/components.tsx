import type { Financial, Summary } from "./api";
import { dateTime, money } from "./format";

export function SummaryCards({ summary }: { summary: Summary }) {
  const cards = [
    { label: "Receitas", value: summary.income, tone: "pos" },
    { label: "Despesas", value: summary.expenses, tone: "neg" },
    { label: "Saldo", value: summary.balance, tone: summary.balance >= 0 ? "pos" : "neg" },
  ];
  return (
    <section className="cards">
      {cards.map((c) => (
        <div className="card" key={c.label}>
          <span className="card-label">{c.label}</span>
          <strong className={`card-value ${c.tone}`}>{money(c.value)}</strong>
        </div>
      ))}
      <div className="card">
        <span className="card-label">Lançamentos</span>
        <strong className="card-value">{summary.count}</strong>
      </div>
    </section>
  );
}

export function AmountChart({ rows }: { rows: Financial[] }) {
  const max = Math.max(1, ...rows.map((r) => Math.abs(r.amount)));
  return (
    <section className="panel">
      <h2>Valores por lançamento</h2>
      {rows.length === 0 && <p className="muted">Sem dados.</p>}
      <ul className="bars">
        {rows.map((r) => (
          <li key={r.id}>
            <span className="bar-label" title={r.description}>{r.description}</span>
            <div className="bar-track">
              <div
                className={`bar ${r.amount >= 0 ? "pos-bg" : "neg-bg"}`}
                style={{ width: `${(Math.abs(r.amount) / max) * 100}%` }}
              />
            </div>
            <span className={`bar-value ${r.amount >= 0 ? "pos" : "neg"}`}>{money(r.amount)}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

interface TableProps {
  rows: Financial[];
  page: number;
  pageSize: number;
  onPage: (p: number) => void;
}

export function FinancialTable({ rows, page, pageSize, onPage }: TableProps) {
  return (
    <section className="panel">
      <h2>Lançamentos</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Descrição</th>
            <th>Origem</th>
            <th>Data</th>
            <th className="num">Valor</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.description}</td>
              <td>{r.source}</td>
              <td>{dateTime(r.date)}</td>
              <td className={`num ${r.amount >= 0 ? "pos" : "neg"}`}>{money(r.amount)}</td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={5} className="muted">Nenhum lançamento nesta página.</td>
            </tr>
          )}
        </tbody>
      </table>
      <div className="pager">
        <button disabled={page === 0} onClick={() => onPage(page - 1)}>← Anterior</button>
        <span>Página {page + 1}</span>
        <button disabled={rows.length < pageSize} onClick={() => onPage(page + 1)}>Próxima →</button>
      </div>
    </section>
  );
}
