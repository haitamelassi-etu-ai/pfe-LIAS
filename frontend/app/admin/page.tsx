"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

type ModerationQueue = {
  publications: { id: number; title: string; year: number }[];
  communications: { id: number; title: string; event: string }[];
};

type ContactMessage = {
  id: number;
  full_name: string;
  email: string;
  subject: string;
};

export default function AdminPage() {
  const [data, setData] = useState<Record<string, number> | null>(null);
  const [queue, setQueue] = useState<ModerationQueue>({ publications: [], communications: [] });
  const [contacts, setContacts] = useState<ContactMessage[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Connectez-vous d'abord comme administrateur.");
      return;
    }

    fetch(`${API_URL}/dashboard/admin`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(async (res) => {
        if (!res.ok) throw new Error("Acces refuse");
        return res.json();
      })
      .then(setData)
      .catch(() => setError("Acces admin non autorise"));

    fetch(`${API_URL}/moderation/queue`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then(setQueue)
      .catch(() => null);

    fetch(`${API_URL}/contact`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then(setContacts)
      .catch(() => null);
  }, []);

  return (
    <main className="container" style={{ paddingTop: 28 }}>
      <h1>Administration</h1>
      {error && <p style={{ color: "#b91c1c" }}>{error}</p>}
      {data && (
        <div className="grid">
          {Object.entries(data).map(([key, value]) => (
            <article key={key} className="card">
              <h3>{key}</h3>
              <p style={{ fontSize: 28, margin: 0 }}>{value}</p>
            </article>
          ))}
        </div>
      )}

      <section className="section card">
        <h2>File de moderation</h2>
        <p>Publications en attente: {(queue.publications || []).length}</p>
        <p>Communications en attente: {(queue.communications || []).length}</p>
      </section>

      <section className="section card">
        <h2>Messages de contact</h2>
        {(contacts || []).slice(0, 5).map((c: ContactMessage) => (
          <article key={c.id} style={{ borderBottom: "1px solid #dde6df", marginBottom: 8 }}>
            <strong>{c.subject}</strong>
            <p>{c.full_name} - {c.email}</p>
          </article>
        ))}
        {!contacts.length && <p>Aucun message pour le moment.</p>}
      </section>
    </main>
  );
}
