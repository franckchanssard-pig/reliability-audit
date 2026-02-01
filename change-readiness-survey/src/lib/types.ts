export interface Question {
  id: string;
  text: string;
  dimension: Dimension;
  isGating: boolean;
}

export type Dimension =
  | "Sponsorship & Leadership"
  | "Value Case & Scope"
  | "Capacity & Roles"
  | "Process & Governance"
  | "Data & Tooling Readiness";

export interface DimensionScore {
  dimension: Dimension;
  score: number;
  avg: number;
  trafficLight: "red" | "orange" | "green";
}

export interface SurveyResults {
  overall: number;
  overallTrafficLight: "red" | "orange" | "green";
  dimensions: DimensionScore[];
  risks: string[];
  recommendations: string[];
  gatingWarnings: string[];
}

export interface ResponseRecord {
  id: string;
  created_at: string;
  company_name: string;
  project_name: string;
  go_live_date: string | null;
  respondent_role: string | null;
  respondent_email: string | null;
  answers_json: string | null;
}

export type Answers = Record<string, number>;
