import { getColorForRisk } from "@/lib/risk";

export type DiseaseResult = {
  name: string;
  risk: number;
  level: string;
  why: string[];
};

export default function RiskCard({ disease }: { disease: DiseaseResult }) {
  const color = getColorForRisk(disease.risk);

  return (
    <div className="rounded-3xl bg-white/5 p-6 shadow-[0_18px_30px_rgba(0,0,0,0.35)]">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white">{disease.name}</h3>
          <span
            className="mt-1 inline-flex rounded-full px-3 py-1 text-xs font-semibold"
            style={{ background: `${color}22`, color }}
          >
            {disease.level}
          </span>
        </div>
        <div className="text-3xl font-semibold text-white">{disease.risk.toFixed(1)}%</div>
      </div>
      <div className="mt-4 text-sm leading-relaxed text-white/70">
        <p className="font-semibold text-white/80">Why?</p>
        <p>{disease.why.length ? disease.why.join(" · ") : "No important factors detected."}</p>
      </div>
    </div>
  );
}
