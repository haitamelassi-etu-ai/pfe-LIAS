"use client";

import { FormEvent, useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

type DashboardData = {
  profile: { id: number; name: string; orcid_id: string | null } | null;
  publications: number;
  communications: number;
};

type MemberDocument = {
  id: number;
  original_name: string;
  size_bytes: number;
  storage_backend: string;
};

export default function MemberDashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [orcid, setOrcid] = useState("");
  const [message, setMessage] = useState("");
  const [documents, setDocuments] = useState<MemberDocument[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;
    fetch(`${API_URL}/dashboard/member`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setOrcid(json?.profile?.orcid_id || "");
      });

    fetch(`${API_URL}/documents/my`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((rows) => setDocuments(rows || []));
  }, []);

  async function linkOrcid(e: FormEvent) {
    e.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) return;

    const res = await fetch(`${API_URL}/orcid/link?orcid_id=${encodeURIComponent(orcid)}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) {
      setMessage("Echec de liaison ORCID");
      return;
    }

    setMessage("ORCID lie avec succes");
  }

  async function importOrcidPublications() {
    const token = localStorage.getItem("token");
    if (!token) return;

    const res = await fetch(`${API_URL}/orcid/import-publications`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
      setMessage("Import ORCID impossible");
      return;
    }
    const json = await res.json();
    setMessage(`${json.imported} publications importees depuis ORCID`);
  }

  async function uploadDocument() {
    const token = localStorage.getItem("token");
    if (!token || !selectedFile) {
      setMessage("Selectionnez un fichier avant upload");
      return;
    }

    const body = new FormData();
    body.append("upload", selectedFile);

    const res = await fetch(`${API_URL}/documents/upload`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body,
    });

    if (!res.ok) {
      setMessage("Upload impossible");
      return;
    }

    const created = await res.json();
    setDocuments((prev) => [created, ...prev]);
    setSelectedFile(null);
    setMessage("Document upload avec succes");
  }

  async function downloadDocument(id: number, filename: string) {
    const token = localStorage.getItem("token");
    if (!token) return;

    const res = await fetch(`${API_URL}/documents/${id}/download`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
      setMessage("Telechargement impossible");
      return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  return (
    <main className="container" style={{ paddingTop: 28 }}>
      <h1>Tableau de bord membre</h1>
      <div className="grid">
        <section className="card">
          <h3>Profil</h3>
          <p>{data?.profile?.name || "Membre"}</p>
          <p>Publications: {data?.publications ?? 0}</p>
          <p>Communications: {data?.communications ?? 0}</p>
        </section>

        <section className="card">
          <h3>ORCID</h3>
          <form onSubmit={linkOrcid} style={{ display: "grid", gap: 10 }}>
            <input
              className="input"
              value={orcid}
              onChange={(e) => setOrcid(e.target.value)}
              placeholder="0000-0000-0000-0000"
            />
            <button className="button" type="submit">
              Lier ORCID
            </button>
          </form>
          <button className="button" style={{ marginTop: 12 }} onClick={importOrcidPublications}>
            Importer publications ORCID
          </button>
          {message && <p>{message}</p>}
        </section>

        <section className="card">
          <h3>Documents scientifiques</h3>
          <input
            className="input"
            type="file"
            onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
          />
          <button className="button" style={{ marginTop: 12 }} onClick={uploadDocument}>
            Uploader document
          </button>

          <div style={{ marginTop: 12 }}>
            {documents.map((doc) => (
              <div key={doc.id} style={{ borderBottom: "1px solid #dde6df", padding: "6px 0" }}>
                <strong>{doc.original_name}</strong>
                <p style={{ margin: "4px 0" }}>
                  {Math.max(1, Math.round(doc.size_bytes / 1024))} KB - {doc.storage_backend}
                </p>
                <button className="button" onClick={() => downloadDocument(doc.id, doc.original_name)}>
                  Telecharger
                </button>
              </div>
            ))}
            {!documents.length && <p>Aucun document depose.</p>}
          </div>
        </section>
      </div>
    </main>
  );
}
