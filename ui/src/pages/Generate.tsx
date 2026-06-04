import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSession } from "../lib/sessionContext";
import { genererPdf } from "../api/client";
import { Card, PageTitle, Spinner, Toast } from "../components/ui/atoms";

export default function Generate() {
  const nav = useNavigate();
  const { state, t } = useSession();
  const m = state.machine;
  const [loading, setLoading] = useState(false);
  const [erreur, setErreur] = useState("");
  const [fait, setFait] = useState(false);

  const coverUrl = m.modele && m.taille ? `/covers/${m.modele}_${m.taille}.png` : "";
  const optionsSel = state.options.filter((o) => o.selected);

  async function generer() {
    setLoading(true);
    setErreur("");
    try {
      const payload = {
        machine: m,
        projet: state.projet,
        performances: state.performances,
        options: state.options,
        contacts: [
          ...state.contacts,
          ...(state.projet.contact_solution ? [state.projet.contact_solution] : []),
        ],
        texte_prescription: state.texte_prescription,
        plans_images: state.plans_images,
      };
      const blob = await genererPdf(payload);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `INVENIO_${state.projet.nom || m.modele + "_" + m.taille}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
      setFait(true);
    } catch (e: any) {
      setErreur(e.message || "Erreur lors de la génération.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-4xl">
      <PageTitle
        titre={t("generate.titre", "Génération de la fiche")}
        sous={t("generate.sous", "Vérifiez l'aperçu, puis générez votre PDF France Air.")}
      />

      <div className="grid gap-6 md:grid-cols-2">
        {/* Aperçu page de garde */}
        <Card className="flex flex-col items-center">
          <span className="label self-start">Aperçu page de garde</span>
          <div className="relative aspect-[210/297] w-full max-w-xs overflow-hidden rounded-xl border border-slate-200 bg-[#eef0f1] dark:border-white/10">
            {coverUrl && (
              <img
                src={coverUrl}
                alt=""
                className="absolute inset-0 h-full w-full object-cover"
                onError={(e) => ((e.target as HTMLImageElement).style.display = "none")}
              />
            )}
            <div className="absolute inset-x-4 bottom-[22%]">
              <div className="text-xl font-extrabold leading-tight text-marine">
                {state.projet.nom || "Fiche de sélection"}
              </div>
              <div className="mt-1 text-sm font-semibold text-electrique">
                {m.modele} {m.taille} · {m.type_machine}
                {m.acoustique ? ` · ${m.acoustique}` : ""}
              </div>
            </div>
          </div>
        </Card>

        {/* Récapitulatif */}
        <Card>
          <span className="label">Récapitulatif</span>
          <dl className="space-y-2 text-sm">
            <Row k="Projet" v={`${state.projet.nom || "—"}${state.projet.numero ? ` (n° ${state.projet.numero})` : ""}`} />
            <Row k="Client" v={state.projet.client?.nom || "—"} />
            <Row k="Machine" v={`${m.modele} ${m.taille} — ${m.fluide} — ${m.medium}`} />
            <Row k="Type" v={`${m.type_machine || "—"} ${m.acoustique || ""}`} />
            <Row k="Performances" v={`${state.performances.length} ligne(s)`} />
            <Row k="Options retenues" v={`${optionsSel.length}`} />
            <Row k="Contacts" v={`${state.contacts.length}`} />
            <Row k="Prescription" v={state.texte_prescription ? "définie" : "manquante"} />
          </dl>
        </Card>
      </div>

      <div className="mt-6 flex items-center justify-between">
        <button className="btn-ghost" onClick={() => nav("/options")}>
          ← Retour
        </button>
        {loading ? (
          <Spinner label="Génération du PDF…" />
        ) : (
          <button className="btn-primary" disabled={!m.modele || !m.taille} onClick={generer}>
            ⬇︎ Générer le PDF
          </button>
        )}
      </div>

      <Toast message={erreur} type="err" />
      {fait && <Toast message="Fiche générée et téléchargée !" />}
    </div>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <div className="flex justify-between gap-4 border-b border-slate-100 pb-1.5 dark:border-white/5">
      <dt className="text-slate-500">{k}</dt>
      <dd className="text-right font-medium">{v}</dd>
    </div>
  );
}
