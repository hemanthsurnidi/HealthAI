export default function PreventionCard({ tip }: { tip: string }) {
  return (
    <div className="rounded-3xl bg-white/5 p-6 shadow-[0_18px_30px_rgba(0,0,0,0.35)]">
      <div className="flex items-center gap-3">
        <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500 to-sky-400 text-white">
          <i className="fas fa-check" />
        </div>
        <p className="text-sm font-semibold text-white/90">{tip}</p>
      </div>
    </div>
  );
}
