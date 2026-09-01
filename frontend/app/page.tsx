"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useMemo, useState } from "react";
import RiskChart from "@/components/RiskChart";
import RiskCard from "@/components/RiskCard";
import PreventionCard from "@/components/PreventionCard";
import StepIndicator from "@/components/StepIndicator";import CustomSelect, { Option } from "../components/CustomSelect";
type Inputs = {
  name: string;
  age: number;
  gender: "male" | "female" | "other";
  heightUnit: "m" | "cm" | "ft";
  heightMeters: number;
  heightCm: number;
  heightFt: number;
  heightIn: number;
  weight: number;
  glucose: number;
  blood_pressure: number;
  cholesterol: number;
  heart_rate: number;
  sleep_hours: number;
  stress_level: number;
  physical_activity: number;
  daily_steps: number;
  smoking: number;
};

type DiseaseResult = {
  name: string;
  risk: number;
  level: string;
  why: string[];
};

type ApiResponse = {
  diseases: DiseaseResult[];
  prevention: string[];
};

const initialInputs: Inputs = {
  name: "",
  age: 45,
  gender: "male",
  heightUnit: "m",
  heightMeters: 1.7,
  heightCm: 170,
  heightFt: 5,
  heightIn: 7,
  weight: 85,
  glucose: 110,
  blood_pressure: 120,
  cholesterol: 210,
  heart_rate: 75,
  sleep_hours: 7.5,
  stress_level: 3,
  physical_activity: 1,
  daily_steps: 8000,
  smoking: 0,
};

const apiBase =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:5000";

const normalizeHeightMeters = (inputs: Inputs) => {
  if (inputs.heightUnit === "cm") return inputs.heightCm / 100;
  if (inputs.heightUnit === "ft") return (inputs.heightFt * 12 + inputs.heightIn) * 0.0254;
  return inputs.heightMeters;
};

const getBmi = (inputs: Inputs) => {
  const h = normalizeHeightMeters(inputs);
  return h > 0 ? inputs.weight / (h * h) : 0;
};

const getRiskLevel = (score: number) => {
  if (score < 30) return { label: "Low", color: "#16A34A" };
  if (score < 60) return { label: "Medium", color: "#EAB308" };
  return { label: "High", color: "#F43F5E" };
};

export default function Page() {
  const [step, setStep] = useState(0);
  const [inputs, setInputs] = useState<Inputs>(initialInputs);
  const [report, setReport] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const bmi = useMemo(() => getBmi(inputs), [inputs]);
  const bmiTag = useMemo(() => {
    if (bmi < 18.5) return { label: "Underweight", tone: "text-emerald-200" };
    if (bmi < 25) return { label: "Normal", tone: "text-sky-200" };
    if (bmi < 30) return { label: "Overweight", tone: "text-amber-200" };
    return { label: "Obese", tone: "text-rose-200" };
  }, [bmi]);

  const overallRisk = useMemo(() => {
    if (!report) return 0;
    return report.diseases.reduce((acc, item) => acc + item.risk, 0) / report.diseases.length;
  }, [report]);

  const goNext = () => setStep((s) => Math.min(4, s + 1));
  const goBack = () => setStep((s) => Math.max(0, s - 1));

  const submit = async () => {
    setLoading(true);
    const payload = {
      name: inputs.name,
      age: inputs.age,
      gender: inputs.gender,
      height: normalizeHeightMeters(inputs),
      weight: inputs.weight,
      bmi: Number(bmi.toFixed(1)),
      glucose: inputs.glucose,
      blood_pressure: inputs.blood_pressure,
      cholesterol: inputs.cholesterol,
      heart_rate: inputs.heart_rate,
      sleep_hours: inputs.sleep_hours,
      stress_level: inputs.stress_level,
      physical_activity: inputs.physical_activity,
      daily_steps: inputs.daily_steps,
      smoking: inputs.smoking,
    };

    try {
      const response = await fetch(`${apiBase}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to retrieve prediction");
      }

      const data: ApiResponse = await response.json();
      setReport(data);
      setStep(3);
    } catch (error) {
      console.error(error);
      alert("Unable to fetch results. Is the backend running on port 5000?");
    } finally {
      setLoading(false);
    }
  };

  const stepContent = (
    <AnimatePresence mode="wait">
      {step === 0 ? (
        <motion.section
          key="welcome"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.35 }}
          className="space-y-8"
        >
          <div className="rounded-3xl bg-surface/70 p-10 shadow-[0_35px_60px_rgba(0,0,0,0.4)]">
            <h2 className="text-3xl font-semibold text-white">Discover your health risks in minutes</h2>
            <p className="mt-3 max-w-2xl text-sm text-white/80">
              Our AI analyzes your profile and lifestyle to deliver personalized risk insights and prevention guidance.
            </p>
            <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center">
              <button
                type="button"
                onClick={goNext}
                className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-indigo-500 via-sky-400 to-orange-400 px-8 py-4 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:-translate-y-[1px] hover:brightness-110"
              >
                Start assessment
              </button>
              <div className="text-sm text-white/70">
                Tip: keep your latest biometrics handy so predictions match your current health.
              </div>
            </div>
          </div>
          <div className="grid gap-6 sm:grid-cols-2">
            <div className="rounded-3xl bg-surface/60 px-6 py-6 shadow-[0_24px_42px_rgba(0,0,0,0.3)]">
              <h3 className="text-lg font-semibold text-white">Six conditions analyzed</h3>
              <p className="mt-3 text-sm text-white/70">
                We predict risk for diabetes, heart disease, hypertension, obesity, sleep disorder, and stroke.
              </p>
            </div>
            <div className="rounded-3xl bg-surface/60 px-6 py-6 shadow-[0_24px_42px_rgba(0,0,0,0.3)]">
              <h3 className="text-lg font-semibold text-white">Actionable insights</h3>
              <p className="mt-3 text-sm text-white/70">
                You’ll get risk details plus prevention steps you can take starting today.
              </p>
            </div>
          </div>
        </motion.section>
      ) : step === 1 ? (
        <motion.section
          key="personal"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.35 }}
          className="space-y-8"
        >
          <div className="rounded-3xl bg-surface/70 p-10 shadow-[0_35px_60px_rgba(0,0,0,0.4)]">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-white">Tell us about yourself</h2>
                <p className="mt-2 text-sm text-white/70">
                  We’ll calculate your BMI and personalize the analysis.
                </p>
              </div>
              <div className="rounded-2xl bg-white/10 px-4 py-3 text-sm font-medium text-white/80">
                BMI:&nbsp;
                <span className="text-lg font-semibold text-white">{bmi.toFixed(1)}</span>
                <span className={`${bmiTag.tone} ml-2 rounded-full bg-white/10 px-2 py-1 text-xs font-semibold`}>
                  {bmiTag.label}
                </span>
              </div>
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-2">
              <div className="grid gap-4">
                <label className="block text-sm font-semibold text-white/80">Name</label>
                <input
                  value={inputs.name}
                  onChange={(e) => setInputs((prev) => ({ ...prev, name: e.target.value }))}
                  className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-white/40 focus:border-sky-300 focus:outline-none"
                  placeholder="Your name"
                />

                <label className="block text-sm font-semibold text-white/80">Age</label>
                <input
                  type="number"
                  min={10}
                  max={100}
                  value={inputs.age}
                  onChange={(e) => setInputs((prev) => ({ ...prev, age: Number(e.target.value) }))}
                  className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-sky-300 focus:outline-none"
                />

                <CustomSelect
                  label="Gender"
                  value={inputs.gender}
                  options={[
                    { label: "Male", value: "male" },
                    { label: "Female", value: "female" },
                    { label: "Other", value: "other" },
                  ]}
                  onChange={(value) => setInputs((prev) => ({ ...prev, gender: value }))}
                />
              </div>

              <div className="grid gap-4">
                <div className="rounded-2xl bg-white/5 p-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-white/80">Height (unit)</p>
                    <div className="flex gap-2">
                      {(["m", "cm", "ft"] as const).map((unit) => (
                        <button
                          key={unit}
                          type="button"
                          onClick={() => setInputs((prev) => ({ ...prev, heightUnit: unit }))}
                          className={`rounded-full px-3 py-1 text-xs font-semibold transition ${
                            inputs.heightUnit === unit
                              ? "bg-gradient-to-r from-indigo-500 via-sky-400 to-orange-400 text-white"
                              : "bg-white/10 text-white/70 hover:bg-white/15"
                          }`}
                        >
                          {unit}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="mt-4 grid gap-3">
                    {inputs.heightUnit === "m" ? (
                      <div>
                        <label className="text-sm font-semibold text-white/80">Meters</label>
                        <input
                          type="number"
                          step={0.01}
                          value={inputs.heightMeters}
                          onChange={(e) =>
                            setInputs((prev) => ({ ...prev, heightMeters: Number(e.target.value) }))
                          }
                          className="mt-2 w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-sky-300 focus:outline-none"
                        />
                      </div>
                    ) : inputs.heightUnit === "cm" ? (
                      <div>
                        <label className="text-sm font-semibold text-white/80">Centimeters</label>
                        <input
                          type="number"
                          step={0.1}
                          value={inputs.heightCm}
                          onChange={(e) =>
                            setInputs((prev) => ({ ...prev, heightCm: Number(e.target.value) }))
                          }
                          className="mt-2 w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-sky-300 focus:outline-none"
                        />
                      </div>
                    ) : (
                      <div className="grid gap-3 sm:grid-cols-2">
                        <div>
                          <label className="text-sm font-semibold text-white/80">Feet</label>
                          <input
                            type="number"
                            min={1}
                            value={inputs.heightFt}
                            onChange={(e) =>
                              setInputs((prev) => ({ ...prev, heightFt: Number(e.target.value) }))
                            }
                            className="mt-2 w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-sky-300 focus:outline-none"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-semibold text-white/80">Inches</label>
                          <input
                            type="number"
                            min={0}
                            max={11}
                            value={inputs.heightIn}
                            onChange={(e) =>
                              setInputs((prev) => ({ ...prev, heightIn: Number(e.target.value) }))
                            }
                            className="mt-2 w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-sky-300 focus:outline-none"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <div className="rounded-2xl bg-white/5 p-4">
                  <label className="text-sm font-semibold text-white/80">Weight (kg)</label>
                  <input
                    type="number"
                    step={0.1}
                    value={inputs.weight}
                    onChange={(e) => setInputs((prev) => ({ ...prev, weight: Number(e.target.value) }))}
                    className="mt-2 w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-sky-300 focus:outline-none"
                  />
                </div>
              </div>
            </div>

            <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <button
                type="button"
                onClick={goBack}
                className="rounded-2xl bg-white/10 px-6 py-3 text-sm font-semibold text-white/80 transition hover:bg-white/15"
              >
                Back
              </button>
              <button
                type="button"
                onClick={goNext}
                className="rounded-2xl bg-gradient-to-r from-indigo-500 via-sky-400 to-orange-400 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:-translate-y-[1px] hover:brightness-110"
              >
                Next: Lifestyle
              </button>
            </div>
          </div>
        </motion.section>
      ) : step === 2 ? (
        <motion.section
          key="lifestyle"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.35 }}
          className="space-y-8"
        >
          <div className="rounded-3xl bg-surface/70 p-10 shadow-[0_35px_60px_rgba(0,0,0,0.4)]">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-white">Health & lifestyle</h2>
                <p className="mt-2 text-sm text-white/70">Select the options that best represent your current habits.</p>
              </div>
              <div className="rounded-2xl bg-white/10 px-4 py-3 text-sm font-medium text-white/80">
                Risk models analyzed: <span className="font-semibold text-white">6</span>
              </div>
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-2">
              {[
                {
                  label: "Blood sugar",
                  value: inputs.glucose,
                  options: [
                    { label: "Low", value: 90 },
                    { label: "Normal", value: 110 },
                    { label: "High", value: 160 },
                    { label: "Don't know", value: 120 },
                  ],
                  onChange: (value: number) => setInputs((prev) => ({ ...prev, glucose: value })),
                  emoji: "💧",
                },
                {
                  label: "Blood pressure",
                  value: inputs.blood_pressure,
                  options: [
                    { label: "Low", value: 90 },
                    { label: "Normal", value: 120 },
                    { label: "High", value: 150 },
                    { label: "Don't know", value: 120 },
                  ],
                  onChange: (value: number) => setInputs((prev) => ({ ...prev, blood_pressure: value })),
                  emoji: "❤️",
                },
                {
                  label: "Cholesterol",
                  value: inputs.cholesterol,
                  options: [
                    { label: "Normal", value: 180 },
                    { label: "High", value: 240 },
                    { label: "Don't know", value: 200 },
                  ],
                  onChange: (value: number) => setInputs((prev) => ({ ...prev, cholesterol: value })),
                  emoji: "💧",
                },
                {
                  label: "Heart rate",
                  value: inputs.heart_rate,
                  options: [
                    { label: "Low", value: 55 },
                    { label: "Normal", value: 75 },
                    { label: "High", value: 95 },
                    { label: "Don't know", value: 75 },
                  ],
                  onChange: (value: number) => setInputs((prev) => ({ ...prev, heart_rate: value })),
                  emoji: "💓",
                },
                {
                  label: "Sleep hours",
                  value: inputs.sleep_hours,
                  options: [
                    { label: "< 5", value: 4 },
                    { label: "5-6", value: 5.5 },
                    { label: "7-8", value: 7.5 },
                    { label: "> 8", value: 9 },
                  ],
                  onChange: (value: number) => setInputs((prev) => ({ ...prev, sleep_hours: value })),
                  emoji: "🛌",
                },
                {
                  label: "Stress level",
                  value: inputs.stress_level,
                  options: [
                    { label: "Low", value: 1 },
                    { label: "Medium", value: 3 },
                    { label: "High", value: 5 },
                  ],
                  onChange: (value: number) => setInputs((prev) => ({ ...prev, stress_level: value })),
                  emoji: "🧠",
                },
                {
                  label: "Physical activity",
                  value: inputs.physical_activity,
                  options: [
                    { label: "None", value: 0 },
                    { label: "Light", value: 1 },
                    { label: "Moderate", value: 2 },
                    { label: "High", value: 3 },
                  ],
                  onChange: (value: number) => setInputs((prev) => ({ ...prev, physical_activity: value })),
                  emoji: "🚶‍♀️",
                },
                {
                  label: "Daily steps",
                  value: inputs.daily_steps,
                  options: [
                    { label: "< 3k", value: 2000 },
                    { label: "3k–6k", value: 4500 },
                    { label: "6k–10k", value: 8000 },
                    { label: "> 10k", value: 12000 },
                  ],
                  onChange: (value: number) => setInputs((prev) => ({ ...prev, daily_steps: value })),
                  emoji: "👟",
                },
                {
                  label: "Smoking",
                  value: inputs.smoking,
                  options: [
                    { label: "No", value: 0 },
                    { label: "Occasionally", value: 1 },
                    { label: "Regularly", value: 1 },
                  ],
                  onChange: (value: number) => setInputs((prev) => ({ ...prev, smoking: value })),
                  emoji: "🚭",
                },
              ].map((field) => (
                <div
                  key={field.label}
                  className="rounded-2xl bg-white/10 p-5 shadow-[0_18px_30px_rgba(0,0,0,0.25)]"
                >
                  <div className="flex items-start gap-3">
                    <div className="grid h-11 w-11 place-items-center rounded-xl bg-white/10 text-lg text-white/90">
                      <span>{field.emoji}</span>
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-white/80">{field.label}</p>
                      <CustomSelect
                        value={field.value}
                        options={field.options as Option<number>[]}
                        onChange={(value) => field.onChange(value)}
                        className="mt-2"
                      />

            <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <button
                type="button"
                onClick={goBack}
                className="rounded-2xl bg-white/10 px-6 py-3 text-sm font-semibold text-white/80 transition hover:bg-white/15"
              >
                Back
              </button>
              <button
                type="button"
                onClick={submit}
                disabled={loading}
                className="rounded-2xl bg-gradient-to-r from-indigo-500 via-sky-400 to-orange-400 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:-translate-y-[1px] hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? "Analyzing..." : "Generate report"}
              </button>
            </div>
          </div>
        </motion.section>
      ) : step === 3 && report ? (
        <motion.section
          key="report"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.35 }}
          className="space-y-8"
        >
          <div className="rounded-3xl bg-surface/70 p-10 shadow-[0_35px_60px_rgba(0,0,0,0.4)]">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-white">Your risk dashboard</h2>
                <p className="mt-2 text-sm text-white/70">
                  Here’s a snapshot of your predicted risks and what’s driving them.
                </p>
              </div>
              <div className="flex flex-col items-start gap-3 rounded-2xl bg-white/10 px-5 py-4 text-white/90 sm:flex-row sm:items-center">
                <div className="flex flex-col">
                  <span className="text-xs text-white/60">Overall risk</span>
                  <span className="text-2xl font-semibold">{overallRisk.toFixed(1)}%</span>
                </div>
                <div className="ml-0 flex items-center gap-2 rounded-full bg-white/10 px-4 py-2 text-sm font-semibold text-white/90 sm:ml-6">
                  <span className="h-2 w-2 rounded-full" style={{ background: getRiskLevel(overallRisk).color }} />
                  {getRiskLevel(overallRisk).label}
                </div>
              </div>
            </div>

            <div className="mt-8">
              <RiskChart data={report.diseases} />
            </div>

            <div className="mt-10 grid gap-6 lg:grid-cols-2">
              {report.diseases.map((d) => (
                <RiskCard key={d.name} disease={d} />
              ))}
            </div>

            <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <button
                type="button"
                onClick={goBack}
                className="rounded-2xl bg-white/10 px-6 py-3 text-sm font-semibold text-white/80 transition hover:bg-white/15"
              >
                Back
              </button>
              <button
                type="button"
                onClick={() => setStep(4)}
                className="rounded-2xl bg-gradient-to-r from-indigo-500 via-sky-400 to-orange-400 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:-translate-y-[1px] hover:brightness-110"
              >
                Next: Prevention
              </button>
            </div>
          </div>
        </motion.section>
      ) : step === 4 && report ? (
        <motion.section
          key="prevention"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.35 }}
          className="space-y-8"
        >
          <div className="rounded-3xl bg-surface/70 p-10 shadow-[0_35px_60px_rgba(0,0,0,0.4)]">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-white">Prevention recommendations</h2>
                <p className="mt-2 text-sm text-white/70">
                  Small changes can have a big impact. Pick a few habits to start with.
                </p>
              </div>
              <div className="rounded-2xl bg-white/10 px-4 py-3 text-sm font-medium text-white/80">
                Recommended steps: <span className="font-semibold text-white">{report.prevention.length}</span>
              </div>
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-2">
              {report.prevention.map((tip) => (
                <PreventionCard key={tip} tip={tip} />
              ))}
            </div>

            <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <button
                type="button"
                onClick={goBack}
                className="rounded-2xl bg-white/10 px-6 py-3 text-sm font-semibold text-white/80 transition hover:bg-white/15"
              >
                Back
              </button>
              <button
                type="button"
                onClick={() => {
                  setStep(0);
                  setReport(null);
                }}
                className="rounded-2xl bg-gradient-to-r from-indigo-500 via-sky-400 to-orange-400 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:-translate-y-[1px] hover:brightness-110"
              >
                Start over
              </button>
            </div>
          </div>
        </motion.section>
      ) : null}
    </AnimatePresence>
  );

  return (
    <section className="mx-auto flex w-full max-w-6xl flex-col gap-10">
      <StepIndicator step={step} />
      {stepContent}
    </section>
  );
}
