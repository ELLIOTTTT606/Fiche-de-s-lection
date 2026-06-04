import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSession, type Option } from "../lib/sessionContext";
import { getOptions, getPrescription } from "../api/options";
import { Card, PageTitle, Spinner } from "../components/ui/atoms";

export default function Options() {
  const nav = useNavigate();
  const { state, update, t } = useSession();
  const [loading, setLoading] = useState(false);
  const [ouverts, setOuverts] = useState<Record<string, boolean>>({});

  useEffect(() => {
    if (!state.machine.modele) return;
    setLoading(true);
    Promise.all([
      getOptions(state.machine.modele),
      getPrescription(state.machine.modele),
    ])
      .then(([catalogue, presc]) => {
        // Fusionne : on garde la sélection issue de la désignation.
        const dejaSel = new Set(state.options.filter((o) => o.selected).map((o) => o.code));
        const fusion: Option[] = catalogue.map((o) => ({
          ...o,
          selected: dejaSel.has(o.code),
        }));
        // Ajoute les options détectées absentes du catalogue.
        state.options
          .filter((o) => o.selected && !catalogue.some((c) => c.code === o.code))
          .forEach((o) => fusion.push(o));
        update({ options: fusion, texte_prescription: presc });
      })
      .catch(() => {
        /* garde les options détectées */
      })
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.machine.modele]);

  const parCategorie = useMemo(() => {
    const map: Record<string, Option[]> = {};
    state.options.forEach((o) => {
      const cat = o.categorie || "Autres";
      (map[cat] ||= []).push(o);
    });
    return map;
  }, [state.options]);

  function toggle(code: string) {
    update({
      options: state.options.map((o) =>
        o.code === code ? { ...o, selected: !o.selected } : o,
      ),
    });
  }

  const nbSel = state.options.filter((o) => o.selected).length;

  return (
    <div className="mx-auto max-w-3xl">
      <PageTitle
        titre={t("options.titre", "Options & accessoires")}
        sous={t("options.sous", "Pré-cochées d'après la désignation. Ajustez si nécessaire.")}
      />

      {loading ? (
        <Card>
          <Spinner label="Chargement du catalogue…" />
        </Card>
      ) : (
        <div className="space-y-3">
          {Object.keys(parCategorie).length === 0 && (
            <Card>
              <p className="text-sm text-slate-500">
                Aucune option au catalogue pour ce modèle. Vous pouvez continuer.
              </p>
            </Card>
          )}
          {Object.entries(parCategorie).map(([cat, opts]) => {
            const open = ouverts[cat] ?? true;
            const sel = opts.filter((o) => o.selected).length;
            return (
              <div key={cat} className="card overflow-hidden">
                <button
                  className="flex w-full items-center justify-between px-5 py-4 text-left"
                  onClick={() => setOuverts((s) => ({ ...s, [cat]: !open }))}
                >
                  <span className="font-semibold text-marine dark:text-white">
                    {cat} <span className="ml-2 text-xs text-slate-400">{sel}/{opts.length}</span>
                  </span>
                  <span className="text-slate-400">{open ? "▾" : "▸"}</span>
                </button>
                {open && (
                  <ul className="divide-y divide-slate-100 dark:divide-white/5">
                    {opts.map((o) => (
                      <li key={o.code || o.libelle} className="px-5 py-3">
                        <label className="flex cursor-pointer items-start gap-3">
                          <input
                            type="checkbox"
                            className="mt-1 h-4 w-4 accent-marine"
                            checked={o.selected}
                            onChange={() => toggle(o.code)}
                          />
                          <span className="flex-1">
                            <span className="font-medium">{o.libelle}</span>
                            {o.code && <span className="ml-2 font-mono text-xs text-slate-400">{o.code}</span>}
                            {o.description && (
                              <span className="block text-sm text-slate-500">{o.description}</span>
                            )}
                            {o.conseil && (
                              <span className="mt-1 block text-xs italic text-electrique">💡 {o.conseil}</span>
                            )}
                          </span>
                          {o.prix != null && (
                            <span className="whitespace-nowrap text-sm font-semibold text-marine dark:text-slate-200">
                              {o.prix.toFixed(2)} €
                            </span>
                          )}
                        </label>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            );
          })}
        </div>
      )}

      <div className="mt-6 flex items-center justify-between">
        <button className="btn-ghost" onClick={() => nav("/contacts")}>
          ← Retour
        </button>
        <span className="text-sm text-slate-500">{nbSel} option(s) retenue(s)</span>
        <button className="btn-primary" onClick={() => nav("/generate")}>
          Continuer →
        </button>
      </div>
    </div>
  );
}
