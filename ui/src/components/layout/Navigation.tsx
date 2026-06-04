import { Link, useLocation } from "react-router-dom";
import { useTheme } from "../../lib/theme";
import { useSession } from "../../lib/sessionContext";

// Étapes du workflow (stepper de progression).
const ETAPES = [
  { path: "/", label: "Import" },
  { path: "/machine", label: "Machine" },
  { path: "/projet", label: "Projet" },
  { path: "/contacts", label: "Contacts" },
  { path: "/options", label: "Options" },
  { path: "/generate", label: "Génération" },
];

export default function Navigation() {
  const { pathname } = useLocation();
  const { theme, toggle } = useTheme();
  const { t } = useSession();
  const idxActif = ETAPES.findIndex((e) => e.path === pathname);

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200/70 bg-white/70 backdrop-blur dark:border-white/10 dark:bg-encre/70">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
        <Link to="/" className="flex items-center gap-2">
          <span className="grid h-8 w-8 place-items-center rounded-lg bg-marine font-extrabold text-white">
            I
          </span>
          <span className="text-lg font-extrabold tracking-tight text-marine dark:text-white">
            INVENIO
          </span>
          <span className="hidden text-xs text-slate-400 sm:inline">· France Air</span>
        </Link>

        {/* Stepper */}
        <nav className="hidden flex-1 items-center justify-center gap-1 md:flex">
          {ETAPES.map((e, i) => {
            const actif = e.path === pathname;
            const fait = idxActif >= 0 && i < idxActif;
            return (
              <Link
                key={e.path}
                to={e.path}
                className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-semibold transition ${
                  actif
                    ? "bg-marine text-white"
                    : fait
                      ? "text-teal"
                      : "text-slate-400 hover:text-marine dark:hover:text-white"
                }`}
              >
                <span
                  className={`grid h-5 w-5 place-items-center rounded-full text-[10px] ${
                    actif ? "bg-white text-marine" : fait ? "bg-teal text-white" : "bg-slate-200 dark:bg-white/10"
                  }`}
                >
                  {fait ? "✓" : i + 1}
                </span>
                {e.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          <Link
            to="/maintenance"
            className="rounded-lg px-3 py-1.5 text-xs font-semibold text-slate-500 hover:text-marine dark:hover:text-white"
            title={t("nav.maintenance", "Maintenance")}
          >
            ⚙︎ {t("nav.maintenance", "Maintenance")}
          </Link>
          <button
            onClick={toggle}
            className="grid h-9 w-9 place-items-center rounded-lg bg-slate-100 text-base hover:bg-slate-200 dark:bg-white/10 dark:hover:bg-white/20"
            title="Thème clair / sombre"
          >
            {theme === "dark" ? "☀︎" : "☾"}
          </button>
        </div>
      </div>
    </header>
  );
}
