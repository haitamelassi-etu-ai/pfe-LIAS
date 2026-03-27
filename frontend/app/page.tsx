import Link from "next/link";

import { apiGet } from "@/lib/api";

type HomeData = {
  news: { id: number; title: string }[];
  events: { id: number; title: string; date: string | null }[];
  publications: { id: number; title: string; year: number }[];
};

export default async function HomePage() {
  let data: HomeData = { news: [], events: [], publications: [] };
  try {
    data = await apiGet<HomeData>("/public/home");
  } catch {
    data = { news: [], events: [], publications: [] };
  }

  return (
    <main className="container">
      <header className="header">
        <h3 className="brand">LIAS Platform</h3>
        <nav className="nav">
          <Link href="/">Accueil</Link>
          <Link href="/publications">Publications</Link>
          <Link href="/search">Recherche</Link>
          <Link href="/contact">Contact</Link>
          <Link href="/login">Espace membre</Link>
          <Link href="/admin">Administration</Link>
        </nav>
      </header>

      <section className="hero">
        <span className="kicker">Plateforme institutionnelle et scientifique</span>
        <h1>Laboratoire LIAS</h1>
        <p>
          Une vitrine claire pour le public et un espace solide pour les chercheurs. Le laboratoire
          centralise ses publications, evenements et profils membres dans une plateforme unique.
        </p>

        <div className="hero-actions">
          <Link href="/publications" className="pill pill-primary">
            Explorer les publications
          </Link>
          <Link href="/register" className="pill pill-secondary">
            Creer un compte membre
          </Link>
        </div>

        <div className="stats">
          <div className="stat">
            <strong>{data.news.length}</strong>
            <span>Actualites</span>
          </div>
          <div className="stat">
            <strong>{data.events.length}</strong>
            <span>Evenements</span>
          </div>
          <div className="stat">
            <strong>{data.publications.length}</strong>
            <span>Publications recentes</span>
          </div>
        </div>
      </section>

      <section className="section">
        <h2 className="title">Actualites</h2>
        <p className="subtitle">Annonces, soutenances, appels et moments forts du laboratoire.</p>
        <div className="grid">
          {data.news.map((item) => (
            <article className="card" key={item.id}>
              <h4>{item.title}</h4>
            </article>
          ))}
          {!data.news.length && <div className="empty">Aucune actualite publiee.</div>}
        </div>
      </section>

      <section className="section">
        <h2 className="title">Evenements</h2>
        <p className="subtitle">Seminaires, workshops et activites scientifiques a venir.</p>
        <div className="grid">
          {data.events.map((item) => (
            <article className="card" key={item.id}>
              <h4>{item.title}</h4>
              <p className="meta">{item.date || "Date a confirmer"}</p>
            </article>
          ))}
          {!data.events.length && <div className="empty">Aucun evenement.</div>}
        </div>
      </section>

      <section className="section">
        <h2 className="title">Publications recentes</h2>
        <p className="subtitle">Travaux valides et valorises par le laboratoire.</p>
        <div className="grid">
          {data.publications.map((item) => (
            <article className="card" key={item.id}>
              <h4>{item.title}</h4>
              <p className="meta">Annee {item.year}</p>
            </article>
          ))}
          {!data.publications.length && <div className="empty">Aucune publication validee.</div>}
        </div>
      </section>

      <footer className="footer">LIAS - Plateforme scientifique institutionnelle</footer>
    </main>
  );
}
