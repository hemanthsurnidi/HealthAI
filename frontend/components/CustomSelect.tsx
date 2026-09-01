"use client";

import { useEffect, useRef, useState } from "react";

export type Option<T extends string | number> = {
  label: string;
  value: T;
};

type CustomSelectProps<T extends string | number> = {
  value: T;
  options: Option<T>[];
  onChange: (value: T) => void;
  className?: string;
  label?: string;
};

export default function CustomSelect<T extends string | number>({
  value,
  options,
  onChange,
  className = "",
  label,
}: CustomSelectProps<T>) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const selected = options.find((opt) => opt.value === value) ?? options[0];

  return (
    <div className={`relative ${className}`} ref={ref}>
      {label ? <div className="text-sm font-semibold text-white/80">{label}</div> : null}
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="mt-2 w-full rounded-2xl border border-white/10 bg-white/90 px-4 py-3 text-left text-slate-900 focus:border-sky-300 focus:outline-none"
      >
        <span className="block truncate">{selected?.label ?? "Select"}</span>
        <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-slate-500">▾</span>
      </button>

      {open ? (
        <ul className="absolute z-20 mt-2 w-full overflow-hidden rounded-2xl border border-white/10 bg-white/95 text-slate-900 shadow-lg">
          {options.map((opt) => (
            <li
              key={opt.label}
              onClick={() => {
                onChange(opt.value);
                setOpen(false);
              }}
              className={`cursor-pointer px-4 py-3 hover:bg-slate-100 ${opt.value === value ? "bg-slate-200" : ""}`}
            >
              {opt.label}
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
