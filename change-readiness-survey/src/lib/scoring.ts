import { Answers, Dimension, DimensionScore, SurveyResults } from "./types";
import { QUESTIONS, DIMENSIONS } from "./questionnaire";

function trafficLight(score: number): "red" | "orange" | "green" {
  if (score < 40) return "red";
  if (score < 70) return "orange";
  return "green";
}

export function computeScores(answers: Answers): SurveyResults {
  const dimensionScores: DimensionScore[] = DIMENSIONS.map((dim) => {
    const dimQuestions = QUESTIONS.filter((q) => q.dimension === dim);
    const values = dimQuestions.map((q) => answers[q.id] ?? 3);
    const avg = values.reduce((a, b) => a + b, 0) / values.length;
    const score = Math.round(((avg - 1) / 4) * 100);
    return { dimension: dim, score, avg, trafficLight: trafficLight(score) };
  });

  const overall = Math.round(
    dimensionScores.reduce((sum, d) => sum + d.score, 0) /
      dimensionScores.length
  );

  const gatingWarnings: string[] = [];
  const gatingQuestions = QUESTIONS.filter((q) => q.isGating);
  for (const q of gatingQuestions) {
    if ((answers[q.id] ?? 3) <= 2) {
      gatingWarnings.push(
        `Gating risk: "${q.text}" scored ${answers[q.id]} (≤2)`
      );
    }
  }

  const risks = buildRisks(dimensionScores, answers);
  const recommendations = buildRecommendations(dimensionScores, answers);

  return {
    overall,
    overallTrafficLight: trafficLight(overall),
    dimensions: dimensionScores,
    risks,
    recommendations,
    gatingWarnings,
  };
}

function getDimScore(
  scores: DimensionScore[],
  dim: Dimension
): DimensionScore {
  return scores.find((s) => s.dimension === dim)!;
}

function buildRisks(scores: DimensionScore[], answers: Answers): string[] {
  const risks: string[] = [];

  // Two lowest dimensions
  const sorted = [...scores].sort((a, b) => a.score - b.score);
  risks.push(
    `Lowest dimension: ${sorted[0].dimension} (${sorted[0].score}/100)`
  );
  if (sorted[1].score < 70) {
    risks.push(
      `Second lowest: ${sorted[1].dimension} (${sorted[1].score}/100)`
    );
  }

  // Gating question failures
  const gatingQuestions = QUESTIONS.filter((q) => q.isGating);
  for (const q of gatingQuestions) {
    if ((answers[q.id] ?? 3) <= 2) {
      risks.push(`Critical gap: "${q.text}" rated ${answers[q.id]}/5`);
    }
  }

  return risks;
}

function buildRecommendations(
  scores: DimensionScore[],
  answers: Answers
): string[] {
  const recs: string[] = [];

  const sponsorship = getDimScore(scores, "Sponsorship & Leadership");
  if (sponsorship.score < 60 || (answers["Q1"] ?? 3) <= 2) {
    recs.push(
      "Establish an active executive sponsor, set up a decision forum, and implement weekly governance cadence."
    );
  }

  const valueCaseScope = getDimScore(scores, "Value Case & Scope");
  if (valueCaseScope.score < 60) {
    recs.push(
      "Define a clear value case with measurable KPIs and enforce a scope freeze to prevent scope creep."
    );
  }

  const capacity = getDimScore(scores, "Capacity & Roles");
  if (capacity.score < 60 || (answers["Q8"] ?? 3) <= 2) {
    recs.push(
      "Create a staffing plan with explicit time allocation for the project and identify change champions."
    );
  }

  const processGov = getDimScore(scores, "Process & Governance");
  if (processGov.score < 60) {
    recs.push(
      "Conduct a process mapping workshop and establish a formal change request process."
    );
  }

  const dataTooling = getDimScore(scores, "Data & Tooling Readiness");
  if (dataTooling.score < 60 || (answers["Q13"] ?? 3) <= 2) {
    recs.push(
      "Complete a data inventory, unblock data access, and create a concrete integration plan for Pigment."
    );
  }

  if (recs.length === 0) {
    recs.push(
      "All dimensions are in good shape. Continue monitoring and maintain stakeholder alignment."
    );
  }

  return recs;
}
