import { apiGet } from "@/lib/api";
import Link from "next/link";

type Publication = {
  id: number;
  title: string;
  authors: string;
  publication_type: string;
  year: number;
};

export default async function PublicationsPage() {
  let items: Publication[] = [];
  try {
    items = await apiGet<Publication[]>("/publications?validated_only=true");
  } catch {
    items = [];
  }

  return (
    <main className="container" style={{ paddingTop: 24 }}>
      <header className="header">
        <h3 className="brand">LIAS Platform</h3>
        <nav className="nav">
          <Link href="/">Accueil</Link>
          <Link href="/publications">Publications</Link>
          <Link href="/search">Recherche</Link>
          <Link href="/contact">Contact</Link>
        </nav>
      </header>

      <section className="hero">
        <span className="kicker">Corpus scientifique</span>
        <h1>Publications du laboratoire</h1>
        <p>
          Inventaire des publications validees: articles, communications, ouvrages et autres
          productions scientifiques.
        </p>
      </section>

      <section className="section">
        <h2 className="title">Liste des publications</h2>
        <p className="subtitle">Resultats valides et accessibles au public.</p>

      <div className="grid">
        {items.map((item) => (
          <article className="card" key={item.id}>
            <h3>{item.title}</h3>
            <p className="meta">{item.authors}</p>
            <p className="meta">
              {item.publication_type} - {item.year}
            </p>
          </article>
        ))}
        {!items.length && <div className="empty">Aucune publication validee pour le moment.</div>}
      </div>
      </section>
    </main>
  );
}
