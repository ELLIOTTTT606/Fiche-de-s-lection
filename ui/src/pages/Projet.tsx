import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSession, type Client } from "../lib/sessionContext";
import { rechercherClients } from "../api/contacts";
import { Card, Field, PageTitle } from "../components/ui/atoms";

export default function Projet() {
  const nav = useNavigate();
  const { state, update, t } = useSession();
  const projet = state.projet;

  const [recherche, setRecherche] = useState(projet.client?.nom || "");
  const [resultats, setResultats] = useState<Client[]>([]);
  const [ouvert, setOuvert] = useState(false);
  const [chargement, setChargement] = useState(false);

  // Autocomplete client (debounce).
  useEffect(() => {
    if (!recherche || recherche.length < 2 || recherche === projet.client?.nom) {
      setResultats([]);
      return;
    }
    setChargement(true);
    const id = setTimeout(() => {
      rechercherClients(recherche)
        .then((r) => {
          setResultats(r);
          setOuvert(true);
        })
        .catch(() => setResultats([]))
        .finally(() => setChargement(false));
    }, 300);
    return () => clearTimeout(id);
  }, [recherche]);

  function setProjet(patch: Partial<typeof projet>) {
    update({ projet: { ...projet, ...patch } });
  }

  function choisirClient(c: Client) {
    setProjet({ client: c });
    setRecherche(c.nom);
    setOuvert(false);
  }

  return (
    <div className="mx-auto max-w-3xl">
      <PageTitle
        titre={t("projet.titre", "Projet & Client")}
        sous={t("projet.sous", "Renseignez le projet et recherchez le client.")}
      />

      <Card>
        <div className="grid gap-5 sm:grid-cols-2">
          <Field label="N° de projet" value={projet.numero} onChange={(v) => setProjet({ numero: v })} placeholder="ex. 2026-0142" />
          <Field label="Nom du projet" value={projet.nom} onChange={(v) => setProjet({ nom: v })} placeholder="ex. Résidence Les Tilleuls" />
        </div>

        <div className="relative mt-5">
          <span className="label">Client</span>
          <input
            className="input"
            value={recherche}
            placeholder="Tapez le nom ou le code du client…"
            onChange={(e) => {
              setRecherche(e.target.value);
              if (projet.client) setProjet({ client: null });
            }}
            onFocus={() => resultats.length && setOuvert(true)}
          />
          {chargement && <p className="mt-1 text-xs text-slate-400">Recherche…</p>}
          {ouvert && resultats.length > 0 && (
            <ul className="absolute z-20 mt-1 max-h-64 w-full overflow-auto rounded-xl border border-slate-200 bg-white shadow-lg dark:border-white/10 dark:bg-encre">
              {resultats.map((c) => (
                <li key={c.id ?? c.code_tiers}>
                  <button
                    className="flex w-full items-center justify-between px-4 py-2.5 text-left text-sm hover:bg-slate-50 dark:hover:bg-white/5"
                    onClick={() => choisirClient(c)}
                  >
                    <span className="font-medium">{c.nom}</span>
                    <span className="font-mono text-xs text-slate-400">
                      {c.code_postal} · dpt {c.departement}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {projet.client && (
          <div className="mt-4 rounded-xl bg-teal/10 px-4 py-3 text-sm">
            <span className="font-semibold text-teal">Client sélectionné :</span>{" "}
            {projet.client.nom} — {projet.client.code_postal} (département {projet.client.departement})
          </div>
        )}
      </Card>

      <div className="mt-6 flex justify-between">
        <button className="btn-ghost" onClick={() => nav("/machine")}>
          ← Retour
        </button>
        <button className="btn-primary" onClick={() => nav("/contacts")}>
          Continuer →
        </button>
      </div>
    </div>
  );
}
