"use client";

import { FormEvent, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function ContactPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setStatus("");

    const res = await fetch(`${API_URL}/contact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ full_name: fullName, email, subject, message }),
    });

    if (!res.ok) {
      setStatus("Echec de l'envoi. Veuillez reessayer.");
      return;
    }

    setStatus("Message envoye avec succes.");
    setFullName("");
    setEmail("");
    setSubject("");
    setMessage("");
  }

  return (
    <main className="container" style={{ maxWidth: 780, paddingTop: 24 }}>
      <h1>Contact laboratoire LIAS</h1>
      <p>Posez votre question ou proposez une collaboration scientifique.</p>

      <form className="card" style={{ display: "grid", gap: 10 }} onSubmit={onSubmit}>
        <input
          className="input"
          placeholder="Nom complet"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          required
        />
        <input
          className="input"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          className="input"
          placeholder="Sujet"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          required
        />
        <textarea
          className="textarea"
          placeholder="Votre message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          rows={6}
          required
        />
        <button className="button" type="submit">
          Envoyer
        </button>
      </form>

      {status && <p>{status}</p>}
    </main>
  );
}
