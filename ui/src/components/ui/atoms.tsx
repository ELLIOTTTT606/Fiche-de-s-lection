import type { ReactNode } from "react";

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <div className={`card p-6 ${className}`}>{children}</div>;
}

export function PageTitle({ titre, sous }: { titre: string; sous?: string }) {
  return (
    <div className="mb-6 animate-fadein">
      <h1 className="text-2xl font-extrabold text-marine dark:text-white sm:text-3xl">{titre}</h1>
      {sous && <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{sous}</p>}
    </div>
  );
}

export function Field({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  type?: string;
}) {
  return (
    <label className="block">
      <span className="label">{label}</span>
      <input
        className="input"
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
      />
    </label>
  );
}

export function Select({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: string[];
}) {
  return (
    <label className="block">
      <span className="label">{label}</span>
      <select className="input" value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">—</option>
        {options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </label>
  );
}

export function Toast({ message, type = "ok" }: { message: string; type?: "ok" | "err" }) {
  if (!message) return null;
  return (
    <div
      className={`fixed bottom-6 left-1/2 z-50 -translate-x-1/2 animate-fadein rounded-xl px-5 py-3 text-sm font-semibold text-white shadow-lg ${
        type === "ok" ? "bg-teal" : "bg-rouge"
      }`}
    >
      {type === "ok" ? "✓ " : "⚠ "}
      {message}
    </div>
  );
}

export function Spinner({ label }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 text-slate-500">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-electrique border-t-transparent" />
      {label && <span className="text-sm">{label}</span>}
    </div>
  );
}
