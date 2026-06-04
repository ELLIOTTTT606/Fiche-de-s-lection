import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSession, type Contact } from "../lib/sessionContext";
import { getContacts } from "../api/contacts";
import { Card, Field, PageTitle, Spinner } from "../components/ui/atoms";

function ContactCard({ c }: { c: Contact }) {
  return (
    <div className="rounded-xl border border-slate-200 p-4 dark:border-white/10">
      <div className="mb-1 inline-block rounded-full bg-marine px-2.5 py-0.5 text-xs font-bold text-white">
        {c.role}
      </div>
      <div className="font-semibold">{c.nom || "—"}</div>
      <div className="text-sm text-slate-500">{c.telephone}</div>
      <div className="text-sm text-slate-500">{c.email}</div>
    </div>
  );
}

export default function Contacts() {
  const nav = useNavigate();
  const { state, update, t } = useSession();
  const [dep, setDep] = useState(
    state.projet.client?.departement || state.contacts[0]?.departement || "",
  );
  const [loading, setLoading] = useState(false);
  const [erreur, setErreur] = useState("");
  const [solution, setSolution] = useState<Contact[]>([]);

  function charger(departement: string) {
    if (!departement) return;
    setLoading(true);
    setErreur("");
    getContacts(departement)
      .then((r) => {
        update({ contacts: r.force_de_vente });
        setSolution(r.solution);
        // Pré-sélection du contact Solution si un seul.
        if (r.solution.length === 1 && !state.projet.contact_solution) {
          update({ projet: { ...state.projet, contact_solution: r.solution[0] } });
        }
      })
      .catch((e) => setErreur(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    if (dep) charger(dep);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const tci = state.contacts.filter((c) => c.role === "TCI");
  const tcs = state.contacts.filter((c) => c.role === "TCS");

  return (
    <div className="mx-auto max-w-3xl">
      <PageTitle
        titre={t("contacts.titre", "Vos contacts")}
        sous={t("contacts.sous", "TCI et TCS du département du client, + contact Solution.")}
      />

      <Card>
        <div className="flex items-end gap-3">
          <div className="w-40">
            <Field label="Département" value={dep} onChange={setDep} placeholder="ex. 69" />
          </div>
          <button className="btn-accent" onClick={() => charger(dep)}>
            Rechercher
          </button>
        </div>

        {loading && (
          <div className="mt-5">
            <Spinner label="Chargement des contacts…" />
          </div>
        )}
        {erreur && <p className="mt-4 text-sm text-rouge">{erreur}</p>}

        {!loading && (
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            {tci.length === 0 && tcs.length === 0 ? (
              <p className="text-sm text-slate-500">Aucun contact trouvé pour ce département.</p>
            ) : (
              [...tci, ...tcs].map((c, i) => <ContactCard key={i} c={c} />)
            )}
          </div>
        )}

        {solution.length > 0 && (
          <div className="mt-6">
            <span className="label">Contact Solution</span>
            <select
              className="input"
              value={state.projet.contact_solution?.nom || ""}
              onChange={(e) => {
                const sel = solution.find((s) => s.nom === e.target.value) || null;
                update({ projet: { ...state.projet, contact_solution: sel } });
              }}
            >
              <option value="">—</option>
              {solution.map((s) => (
                <option key={s.nom} value={s.nom}>
                  {s.nom} {s.telephone ? `· ${s.telephone}` : ""}
                </option>
              ))}
            </select>
          </div>
        )}
      </Card>

      <div className="mt-6 flex justify-between">
        <button className="btn-ghost" onClick={() => nav("/projet")}>
          ← Retour
        </button>
        <button className="btn-primary" onClick={() => nav("/options")}>
          Continuer →
        </button>
      </div>
    </div>
  );
}
