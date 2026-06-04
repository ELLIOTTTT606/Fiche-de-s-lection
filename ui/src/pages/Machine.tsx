import { useNavigate } from "react-router-dom";
import { useSession } from "../lib/sessionContext";
import { ACOUSTIQUES, MACHINES, MODELES, TYPES_MACHINE, infoModele } from "../lib/machines";
import { Card, PageTitle, Select } from "../components/ui/atoms";

export default function Machine() {
  const nav = useNavigate();
  const { state, update, t } = useSession();
  const m = state.machine;

  const tailles = infoModele(m.modele)?.tailles || [];

  function setM(patch: Partial<typeof m>) {
    const next = { ...m, ...patch };
    // Recalcule fluide/medium quand le modèle change.
    if (patch.modele) {
      const info = MACHINES.find((x) => x.modele === patch.modele);
      next.fluide = info?.fluide || "";
      next.medium = info?.medium || "";
      next.taille = "";
    }
    update({ machine: next });
  }

  return (
    <div className="mx-auto max-w-3xl">
      <PageTitle
        titre={t("machine.titre", "Confirmez la machine")}
        sous={t("machine.sous", "Détecté automatiquement depuis la désignation. Modifiable si besoin.")}
      />

      {m.designation && (
        <p className="mb-4 rounded-xl bg-marine/5 px-4 py-2 font-mono text-sm text-marine dark:bg-white/5 dark:text-slate-200">
          {m.designation}
        </p>
      )}

      <Card>
        <div className="grid gap-5 sm:grid-cols-2">
          <Select label="Modèle" value={m.modele} onChange={(v) => setM({ modele: v })} options={MODELES} />
          <Select label="Taille" value={m.taille} onChange={(v) => setM({ taille: v })} options={tailles} />
          <Select
            label="Type de machine"
            value={m.type_machine}
            onChange={(v) => setM({ type_machine: v })}
            options={[...TYPES_MACHINE]}
          />
          <Select
            label="Acoustique"
            value={m.acoustique}
            onChange={(v) => setM({ acoustique: v })}
            options={[...ACOUSTIQUES]}
          />
        </div>

        <div className="mt-5 flex flex-wrap gap-2">
          {m.fluide && <span className="chip">Fluide {m.fluide}</span>}
          {m.medium && <span className="chip">{m.medium}</span>}
        </div>
      </Card>

      <div className="mt-6 flex justify-between">
        <button className="btn-ghost" onClick={() => nav("/")}>
          ← Retour
        </button>
        <button
          className="btn-primary"
          disabled={!m.modele || !m.taille}
          onClick={() => nav("/projet")}
        >
          Continuer →
        </button>
      </div>
    </div>
  );
}
