import { useEffect, useState } from "react";
import * as M from "../api/maintenance";
import { MODELES } from "../lib/machines";
import { PageTitle, Toast } from "../components/ui/atoms";

type OngletId = "contacts" | "options" | "prescriptions" | "designation" | "clients" | "libelles";

const ONGLETS: { id: OngletId; label: string; icone: string }[] = [
  { id: "contacts", label: "Contacts commerciaux", icone: "👥" },
  { id: "options", label: "Options & accessoires", icone: "🧩" },
  { id: "prescriptions", label: "Textes de prescription", icone: "📝" },
  { id: "designation", label: "Décodage désignation", icone: "🔠" },
  { id: "clients", label: "Clients", icone: "🏢" },
  { id: "libelles", label: "Textes de l'interface", icone: "🏷️" },
];

export default function Maintenance() {
  const [deverrouille, setDeverrouille] = useState(!!M.getMotDePasse());
  const [mdp, setMdp] = useState("");
  const [erreur, setErreur] = useState("");
  const [onglet, setOnglet] = useState<OngletId>("contacts");
  const [toast, setToast] = useState("");

  function notif(msg: string) {
    setToast(msg);
    setTimeout(() => setToast(""), 2500);
  }

  async function connexion() {
    setErreur("");
    const ok = await M.login(mdp);
    if (ok) setDeverrouille(true);
    else setErreur("Mot de passe incorrect.");
  }

  if (!deverrouille) {
    return (
      <div className="mx-auto mt-12 max-w-sm">
        <div className="card p-8 text-center">
          <div className="mb-4 text-4xl">🔒</div>
          <h1 className="mb-1 text-xl font-extrabold text-marine dark:text-white">Maintenance</h1>
          <p className="mb-6 text-sm text-slate-500">
            Espace réservé. Entrez le mot de passe pour modifier les données.
          </p>
          <input
            className="input mb-3"
            type="password"
            value={mdp}
            placeholder="Mot de passe"
            onChange={(e) => setMdp(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && connexion()}
          />
          {erreur && <p className="mb-3 text-sm text-rouge">{erreur}</p>}
          <button className="btn-primary w-full" onClick={connexion}>
            Déverrouiller
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <PageTitle
        titre="Maintenance"
        sous="Modifiez les données d'INVENIO. Tout est enregistré automatiquement, sans coder."
      />

      <div className="mb-6 flex flex-wrap gap-2">
        {ONGLETS.map((o) => (
          <button
            key={o.id}
            onClick={() => setOnglet(o.id)}
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
              onglet === o.id
                ? "bg-marine text-white"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-white/10 dark:text-slate-300 dark:hover:bg-white/20"
            }`}
          >
            <span className="mr-1">{o.icone}</span>
            {o.label}
          </button>
        ))}
      </div>

      <div className="card p-6">
        {onglet === "contacts" && <OngletContacts notif={notif} />}
        {onglet === "options" && <OngletOptions notif={notif} />}
        {onglet === "prescriptions" && <OngletPrescriptions notif={notif} />}
        {onglet === "designation" && <OngletDesignation notif={notif} />}
        {onglet === "clients" && <OngletClients notif={notif} />}
        {onglet === "libelles" && <OngletLibelles notif={notif} />}
      </div>

      <Toast message={toast} />
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Onglet 1 — Contacts (lecture par département)
// ─────────────────────────────────────────────────────────────
function OngletContacts({ notif }: { notif: (m: string) => void }) {
  const [dep, setDep] = useState("");
  const [fv, setFv] = useState<any[]>([]);
  const [sol, setSol] = useState<any[]>([]);
  const [erreur, setErreur] = useState("");

  function charger() {
    setErreur("");
    M.getContactsMaint(dep)
      .then((r) => {
        setFv(r.force_de_vente);
        setSol(r.solution);
        notif("Contacts chargés");
      })
      .catch((e) => setErreur(e.message));
  }

  return (
    <div>
      <p className="mb-4 text-sm text-slate-500">
        Consultez les contacts TCI / TCS par département, et les contacts Solution.
        Les contacts proviennent de vos tableaux France Air.
      </p>
      <div className="mb-4 flex items-end gap-3">
        <div className="w-40">
          <span className="label">Département</span>
          <input className="input" value={dep} placeholder="ex. 69" onChange={(e) => setDep(e.target.value)} />
        </div>
        <button className="btn-accent" onClick={charger}>
          Afficher
        </button>
      </div>
      {erreur && <p className="text-sm text-rouge">{erreur}</p>}

      <TableSimple
        titre="Force de vente (TCI / TCS)"
        colonnes={["Rôle", "Nom", "Téléphone", "Email", "Dpt"]}
        lignes={fv.map((c) => [c.role, c.nom, c.telephone, c.email, c.departement])}
      />
      <TableSimple
        titre="Contacts Solution"
        colonnes={["Nom", "Téléphone", "Email", "Zone"]}
        lignes={sol.map((c) => [c.nom, c.telephone, c.email, c.departement])}
      />
    </div>
  );
}

function TableSimple({
  titre,
  colonnes,
  lignes,
}: {
  titre: string;
  colonnes: string[];
  lignes: (string | number)[][];
}) {
  return (
    <div className="mt-5">
      <h3 className="mb-2 font-semibold text-marine dark:text-white">{titre}</h3>
      <div className="overflow-x-auto rounded-xl border border-slate-200 dark:border-white/10">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 dark:bg-white/5">
            <tr>
              {colonnes.map((c) => (
                <th key={c} className="px-3 py-2 text-left font-semibold">
                  {c}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {lignes.length === 0 ? (
              <tr>
                <td colSpan={colonnes.length} className="px-3 py-4 text-center text-slate-400">
                  Aucune donnée
                </td>
              </tr>
            ) : (
              lignes.map((l, i) => (
                <tr key={i} className="border-t border-slate-100 dark:border-white/5">
                  {l.map((v, j) => (
                    <td key={j} className="px-3 py-2">
                      {v || "—"}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Onglet 2 — Options (CRUD)
// ─────────────────────────────────────────────────────────────
const CHAMPS_OPTION = [
  { cle: "code", label: "Code" },
  { cle: "libelle", label: "Libellé" },
  { cle: "categorie", label: "Catégorie" },
  { cle: "description", label: "Description" },
  { cle: "conseil", label: "Conseil" },
  { cle: "prix", label: "Prix" },
];

function OngletOptions({ notif }: { notif: (m: string) => void }) {
  return (
    <CrudTable
      notif={notif}
      titre="Catalogue d'options & accessoires"
      aide="Ajoutez, modifiez ou supprimez les options proposées aux commerciaux."
      champs={CHAMPS_OPTION}
      charger={() => M.getOptionsMaint("")}
      creer={M.createOption}
      modifier={M.updateOption}
      supprimer={M.deleteOption}
      filtreModele
    />
  );
}

// ─────────────────────────────────────────────────────────────
// Onglet 3 — Prescriptions (un texte par modèle)
// ─────────────────────────────────────────────────────────────
function OngletPrescriptions({ notif }: { notif: (m: string) => void }) {
  const [modele, setModele] = useState(MODELES[0]);
  const [texte, setTexte] = useState("");
  const [tous, setTous] = useState<any[]>([]);
  const [apercu, setApercu] = useState(false);

  useEffect(() => {
    M.getPrescriptions().then(setTous).catch(() => {});
  }, []);

  useEffect(() => {
    const t = tous.find((p) => (p.modele || "").toUpperCase() === modele);
    setTexte(t?.texte_prescription || "");
  }, [modele, tous]);

  async function sauver() {
    await M.savePrescription(modele, texte);
    const t = await M.getPrescriptions();
    setTous(t);
    notif("Texte de prescription enregistré");
  }

  return (
    <div>
      <p className="mb-4 text-sm text-slate-500">
        Écrivez le texte de prescription affiché dans le PDF, pour chaque modèle.
      </p>
      <div className="mb-3 flex flex-wrap items-end gap-3">
        <div className="w-48">
          <span className="label">Modèle</span>
          <select className="input" value={modele} onChange={(e) => setModele(e.target.value)}>
            {MODELES.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </div>
        <button className="btn-ghost" onClick={() => setApercu((a) => !a)}>
          {apercu ? "Masquer l'aperçu" : "Aperçu"}
        </button>
      </div>

      <textarea
        className="input min-h-[220px]"
        value={texte}
        onChange={(e) => setTexte(e.target.value)}
        placeholder="Saisissez le texte de prescription en français…"
      />

      {apercu && (
        <div className="mt-3 rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm dark:border-white/10 dark:bg-white/5">
          <div className="mb-1 text-xs font-semibold text-slate-400">Aperçu</div>
          <p className="whitespace-pre-line text-justify">{texte || "—"}</p>
        </div>
      )}

      <div className="mt-4 flex justify-end">
        <button className="btn-primary" onClick={sauver}>
          ✓ Enregistrer
        </button>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Onglet 4 — Décodage désignation (CRUD)
// ─────────────────────────────────────────────────────────────
const CHAMPS_DESIGNATION = [
  { cle: "position_start", label: "Position début" },
  { cle: "position_end", label: "Position fin" },
  { cle: "code_attendu", label: "Code attendu" },
  { cle: "option_label", label: "Option" },
  { cle: "categorie", label: "Catégorie" },
  { cle: "modele", label: "Modèle" },
];

function OngletDesignation({ notif }: { notif: (m: string) => void }) {
  return (
    <CrudTable
      notif={notif}
      titre="Décodage de la désignation"
      aide="À la position indiquée dans la désignation, le code attendu correspond à une option. Adaptez ce tableau si GALLETTI change son format — sans coder."
      champs={CHAMPS_DESIGNATION}
      charger={() => M.getDesignation("")}
      creer={M.createDesignation}
      modifier={M.updateDesignation}
      supprimer={M.deleteDesignation}
    />
  );
}

// ─────────────────────────────────────────────────────────────
// Onglet 5 — Clients (CRUD partiel : pas de suppression)
// ─────────────────────────────────────────────────────────────
const CHAMPS_CLIENT = [
  { cle: "code_tiers", label: "Code tiers" },
  { cle: "nom", label: "Nom" },
  { cle: "code_postal", label: "Code postal" },
  { cle: "departement", label: "Département" },
];

function OngletClients({ notif }: { notif: (m: string) => void }) {
  return (
    <CrudTable
      notif={notif}
      titre="Clients"
      aide="Recherchez, ajoutez ou modifiez les clients."
      champs={CHAMPS_CLIENT}
      charger={() => M.getClientsMaint("")}
      creer={M.createClient}
      modifier={M.updateClient}
      recherche={(q) => M.getClientsMaint(q)}
    />
  );
}

// ─────────────────────────────────────────────────────────────
// Onglet 6 — Libellés UI (CRUD)
// ─────────────────────────────────────────────────────────────
const CHAMPS_LIBELLE = [
  { cle: "cle", label: "Identifiant" },
  { cle: "valeur", label: "Texte affiché" },
  { cle: "page", label: "Page" },
];

function OngletLibelles({ notif }: { notif: (m: string) => void }) {
  return (
    <CrudTable
      notif={notif}
      titre="Textes de l'interface"
      aide="Modifiez les mots affichés dans l'application (titres, boutons…). L'identifiant relie le texte à un emplacement ; ne le changez pas, modifiez le « Texte affiché »."
      champs={CHAMPS_LIBELLE}
      charger={M.getLibellesMaint}
      creer={(d) => M.saveLibelle(d.cle, d.valeur, d.page)}
      modifier={(_id, d) => M.saveLibelle(d.cle, d.valeur, d.page)}
      supprimer={M.deleteLibelle}
    />
  );
}

// ─────────────────────────────────────────────────────────────
// Tableau CRUD générique réutilisable
// ─────────────────────────────────────────────────────────────
interface Champ {
  cle: string;
  label: string;
}

function CrudTable({
  notif,
  titre,
  aide,
  champs,
  charger,
  creer,
  modifier,
  supprimer,
  recherche,
  filtreModele,
}: {
  notif: (m: string) => void;
  titre: string;
  aide: string;
  champs: Champ[];
  charger: () => Promise<any[]>;
  creer: (data: any) => Promise<any>;
  modifier: (id: number, data: any) => Promise<any>;
  supprimer?: (id: number) => Promise<any>;
  recherche?: (q: string) => Promise<any[]>;
  filtreModele?: boolean;
}) {
  const [lignes, setLignes] = useState<any[]>([]);
  const [editId, setEditId] = useState<number | "new" | null>(null);
  const [brouillon, setBrouillon] = useState<any>({});
  const [q, setQ] = useState("");
  const [erreur, setErreur] = useState("");
  const [filtre, setFiltre] = useState("");

  function recharger() {
    setErreur("");
    charger()
      .then(setLignes)
      .catch((e) => setErreur(e.message));
  }

  useEffect(recharger, []);

  function nouvelle() {
    setBrouillon({});
    setEditId("new");
  }

  function editer(l: any) {
    setBrouillon({ ...l });
    setEditId(l.id);
  }

  async function valider() {
    setErreur("");
    try {
      if (editId === "new") await creer(brouillon);
      else if (typeof editId === "number") await modifier(editId, brouillon);
      setEditId(null);
      recharger();
      notif("✓ Enregistré");
    } catch (e: any) {
      setErreur(e.message);
    }
  }

  async function effacer(id: number) {
    if (!supprimer) return;
    if (!confirm("Supprimer cette ligne ?")) return;
    try {
      await supprimer(id);
      recharger();
      notif("Ligne supprimée");
    } catch (e: any) {
      setErreur(e.message);
    }
  }

  async function lancerRecherche() {
    if (!recherche) return;
    try {
      setLignes(await recherche(q));
    } catch (e: any) {
      setErreur(e.message);
    }
  }

  const visibles = filtreModele && filtre
    ? lignes.filter((l) => (l.modele || "").toUpperCase().includes(filtre.toUpperCase()))
    : lignes;

  return (
    <div>
      <div className="mb-1 flex items-center justify-between">
        <h3 className="font-semibold text-marine dark:text-white">{titre}</h3>
        <button className="btn-primary" onClick={nouvelle}>
          + Ajouter
        </button>
      </div>
      <p className="mb-4 text-sm text-slate-500">{aide}</p>

      <div className="mb-3 flex flex-wrap gap-3">
        {recherche && (
          <div className="flex items-end gap-2">
            <input
              className="input w-64"
              placeholder="Rechercher…"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && lancerRecherche()}
            />
            <button className="btn-ghost" onClick={lancerRecherche}>
              Chercher
            </button>
          </div>
        )}
        {filtreModele && (
          <div className="flex items-end gap-2">
            <select className="input w-48" value={filtre} onChange={(e) => setFiltre(e.target.value)}>
              <option value="">Tous les modèles</option>
              {MODELES.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {erreur && <p className="mb-3 text-sm text-rouge">{erreur}</p>}

      {/* Formulaire d'édition / création */}
      {editId !== null && (
        <div className="mb-4 rounded-xl border border-electrique/40 bg-electrique/5 p-4">
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {champs.map((c) => (
              <label key={c.cle} className="block">
                <span className="label">{c.label}</span>
                <input
                  className="input"
                  value={brouillon[c.cle] ?? ""}
                  onChange={(e) => setBrouillon({ ...brouillon, [c.cle]: e.target.value })}
                />
              </label>
            ))}
          </div>
          <div className="mt-3 flex justify-end gap-2">
            <button className="btn-ghost" onClick={() => setEditId(null)}>
              Annuler
            </button>
            <button className="btn-primary" onClick={valider}>
              ✓ Enregistrer
            </button>
          </div>
        </div>
      )}

      <div className="overflow-x-auto rounded-xl border border-slate-200 dark:border-white/10">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 dark:bg-white/5">
            <tr>
              {champs.map((c) => (
                <th key={c.cle} className="px-3 py-2 text-left font-semibold">
                  {c.label}
                </th>
              ))}
              <th className="px-3 py-2 text-right font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {visibles.length === 0 ? (
              <tr>
                <td colSpan={champs.length + 1} className="px-3 py-5 text-center text-slate-400">
                  Aucune donnée. Cliquez sur « Ajouter ».
                </td>
              </tr>
            ) : (
              visibles.map((l) => (
                <tr key={l.id} className="border-t border-slate-100 dark:border-white/5">
                  {champs.map((c) => (
                    <td key={c.cle} className="px-3 py-2">
                      {String(l[c.cle] ?? "—")}
                    </td>
                  ))}
                  <td className="px-3 py-2 text-right">
                    <button
                      className="mr-1 rounded-lg px-2 py-1 text-slate-500 hover:bg-slate-100 dark:hover:bg-white/10"
                      title="Modifier"
                      onClick={() => editer(l)}
                    >
                      ✎
                    </button>
                    {supprimer && (
                      <button
                        className="rounded-lg px-2 py-1 text-rouge hover:bg-rouge/10"
                        title="Supprimer"
                        onClick={() => effacer(l.id)}
                      >
                        🗑
                      </button>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
