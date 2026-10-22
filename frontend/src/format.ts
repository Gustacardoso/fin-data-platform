const brl = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

export const money = (v: number) => brl.format(v);
export const dateTime = (iso: string) => new Date(iso).toLocaleString("pt-BR");
