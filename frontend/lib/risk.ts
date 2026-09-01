export const getColorForRisk = (score: number) => {
  if (score < 30) return "#16A34A";
  if (score < 60) return "#EAB308";
  return "#F43F5E";
};
