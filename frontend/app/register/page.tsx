"use client";

import { FormEvent, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function RegisterPage() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("member");
  const [message, setMessage] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();

    const res = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        first_name: firstName,
        last_name: lastName,
        email,
        password,
        role,
      }),
    });

    if (!res.ok) {
      setMessage("Inscription echouee");
      return;
    }

    const data = await res.json();
    localStorage.setItem("token", data.access_token);
    setMessage("Inscription reussie");
  }

  return (
    <main className="container" style={{ maxWidth: 560, paddingTop: 24 }}>
      <h1>Creation de compte membre</h1>
      <form className="card" style={{ display: "grid", gap: 10 }} onSubmit={onSubmit}>
        <input className="input" placeholder="Prenom" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
        <input className="input" placeholder="Nom" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
        <input className="input" placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input className="input" placeholder="Mot de passe" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <select className="select" value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="member">Membre</option>
          <option value="doctorant">Doctorant</option>
        </select>
        <button className="button" type="submit">
          S&apos;inscrire
        </button>
      </form>
      {message && <p>{message}</p>}
    </main>
  );
}
