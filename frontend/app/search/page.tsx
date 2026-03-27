"use client";

import { FormEvent, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function SearchPage() {
  const [q, setQ] = useState("");
  const [result, setResult] = useState<any>(null);

  async function runSearch(e: FormEvent) {
    e.preventDefault();
    if (!q.trim()) return;
    const res = await fetch(`${API_URL}/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    setResult(data);
  }

  return (
    <main className="container" style={{ paddingTop: 24 }}>
      <h1>Recherche multicritere</h1>
      <form onSubmit={runSearch} className="card" style={{ display: "grid", gap: 8 }}>
        <input className="input" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Nom, publication, projet..." />
        <button className="button" type="submit">
          Rechercher
        </button>
      </form>

      {result && (
        <div className="grid" style={{ marginTop: 16 }}>
          <section className="card">
            <h3>Membres</h3>
            {(result.members || []).map((m: any) => (
              <p key={m.id}>{m.name}</p>
            ))}
          </section>

          <section className="card">
            <h3>Publications</h3>
            {(result.publications || []).map((p: any) => (
              <p key={p.id}>{p.title}</p>
            ))}
          </section>

          <section className="card">
            <h3>Projets</h3>
            {(result.projects || []).map((p: any) => (
              <p key={p.id}>{p.title}</p>
            ))}
          </section>

          <section className="card">
            <h3>Evenements</h3>
            {(result.events || []).map((e: any) => (
              <p key={e.id}>{e.title}</p>
            ))}
          </section>
        </div>
      )}
    </main>
  );
}
