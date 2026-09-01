const steps = [
  { label: "Welcome" },
  { label: "Personal" },
  { label: "Lifestyle" },
  { label: "Report" },
  { label: "Prevention" },
];

export default function StepIndicator({ step }: { step: number }) {
  return (
    <div className="flex flex-wrap items-center justify-center gap-3 rounded-3xl bg-white/10 px-4 py-3 text-sm text-white/70 shadow-[0_24px_40px_rgba(0,0,0,0.35)]">
      {steps.map((item, index) => {
        const active = index === step;
        const completed = index < step;
        const baseClasses = "flex items-center gap-2 rounded-full px-3 py-2";
        const stateClasses = completed
          ? "bg-gradient-to-r from-indigo-500 via-sky-400 to-orange-400 text-white"
          : "bg-white/10";
        const activeClasses = active ? "ring-2 ring-white/30" : "";

        return (
          <div key={item.label} className={`${baseClasses} ${stateClasses} ${activeClasses}`}>
            <div className="flex h-6 w-6 items-center justify-center rounded-full bg-white/10 text-xs font-semibold">
              {completed ? "✓" : index + 1}
            </div>
            <span>{item.label}</span>
          </div>
        );
      })}
    </div>
  );
}
