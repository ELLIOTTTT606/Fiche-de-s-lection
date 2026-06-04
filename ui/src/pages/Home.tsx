import { useState, type DragEvent } from "react";
import { useNavigate } from "react-router-dom";
import { parseFichier } from "../api/client";
import { useSession, type Option } from "../lib/sessionContext";
import { Card, PageTitle, Spinner, Toast } from "../components/ui/atoms";

export default function Home() {
  const nav = useNavigate();
  const { update, reset, t } = useSession();
  const [drag, setDrag] = useState(false);
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [erreur, setErreur] = useState("");

  async function traiter(file: File) {
    reset();
    setErreur("");
    setLoading(true);
    setProgress(15);
    const timer = setInterval(() => setProgress((p) => Math.min(p + 10, 85)), 250);
    try {
      const res = await parseFichier(file);
      clearInterval(timer);
      setProgress(100);

      // Fusionne options du catalogue + options détectées par la désignation.
      const detectees: Option[] = (res.options_detectees || []).map((o: any) => ({
        ...o,
        selected: true,
      }));

      update({
        machine: res.machine,
        performances: res.performances || [],
        options: detectees,
        warnings: res.warnings || [],
      });
      setTimeout(() => nav("/machine"), 350);
    } catch (e: any) {
      clearInterval(timer);
      setErreur(e.message || "Échec de l'analyse du fichier.");
      setLoading(false);
      setProgress(0);
    }
  }

  function onDrop(e: DragEvent) {
    e.preventDefault();
    setDrag(false);
    const file = e.dataTransfer.files?.[0];
    if (file) traiter(file);
  }

  return (
    <div className="mx-auto max-w-3xl">
      <PageTitle
        titre={t("home.titre", "Générez vos fiches de sélection")}
        sous={t(
          "home.sous",
          "Déposez une fiche technique GALLETTI (DOCX ou PDF). INVENIO l'analyse et prépare votre fiche de sélection France Air.",
        )}
      />

      <Card>
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDrag(true);
          }}
          onDragLeave={() => setDrag(false)}
          onDrop={onDrop}
          className={`flex flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-16 text-center transition ${
            drag
              ? "border-electrique bg-electrique/5"
              : "border-slate-300 dark:border-white/15"
          }`}
        >
          {loading ? (
            <div className="w-full max-w-sm space-y-4">
              <Spinner label={t("home.analyse", "Analyse du document en cours…")} />
              <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-white/10">
                <div
                  className="h-full bg-electrique transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          ) : (
            <>
              <div className="mb-4 text-5xl">📄</div>
              <p className="mb-1 text-lg font-semibold text-marine dark:text-white">
                {t("home.depot", "Glissez votre fiche GALLETTI ici")}
              </p>
              <p className="mb-5 text-sm text-slate-500">DOCX ou PDF · analyse automatique</p>
              <label className="btn-primary cursor-pointer">
                {t("home.parcourir", "Parcourir mes fichiers")}
                <input
                  type="file"
                  accept=".docx,.pdf"
                  className="hidden"
                  onChange={(e) => e.target.files?.[0] && traiter(e.target.files[0])}
                />
              </label>
            </>
          )}
        </div>
      </Card>

      <Toast message={erreur} type="err" />
    </div>
  );
}
