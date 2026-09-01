import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getColorForRisk } from "@/lib/risk";
import type { DiseaseResult } from "@/components/RiskCard";

export default function RiskChart({ data }: { data: DiseaseResult[] }) {
  return (
    <div className="h-[280px] rounded-3xl bg-white/5 p-6 shadow-[0_18px_30px_rgba(0,0,0,0.35)]">
      <h3 className="text-lg font-semibold text-white">Risk breakdown</h3>
      <p className="mt-1 text-sm text-white/70">Higher bars indicate higher predicted risk for each condition.</p>

      <div className="mt-6 h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 0, right: 16, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="name" tick={{ fill: "rgba(255,255,255,0.7)", fontSize: 12 }} />
            <YAxis tick={{ fill: "rgba(255,255,255,0.7)", fontSize: 12 }} domain={[0, 100]} />
            <Tooltip
              contentStyle={{ background: "rgba(0,0,0,0.85)", border: "1px solid rgba(255,255,255,0.12)" }}
              labelStyle={{ color: "#fff" }}
              itemStyle={{ color: "#fff" }}
            />
            <Bar dataKey="risk" radius={[12, 12, 0, 0]}>
              {data.map((entry) => (
                <Cell key={entry.name} fill={getColorForRisk(entry.risk)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
