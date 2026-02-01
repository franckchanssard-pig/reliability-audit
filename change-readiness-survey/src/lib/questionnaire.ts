import { Question, Dimension } from "./types";

export const DIMENSIONS: Dimension[] = [
  "Sponsorship & Leadership",
  "Value Case & Scope",
  "Capacity & Roles",
  "Process & Governance",
  "Data & Tooling Readiness",
];

export const QUESTIONS: Question[] = [
  // A) Sponsorship & Leadership
  {
    id: "Q1",
    text: "An executive sponsor is identified and actively engaged.",
    dimension: "Sponsorship & Leadership",
    isGating: true,
  },
  {
    id: "Q2",
    text: "Decision-makers are aligned on objectives and timeline.",
    dimension: "Sponsorship & Leadership",
    isGating: false,
  },
  {
    id: "Q3",
    text: "Frontline managers support the change and will reinforce it.",
    dimension: "Sponsorship & Leadership",
    isGating: false,
  },

  // B) Value Case & Scope
  {
    id: "Q4",
    text: "Business outcomes and success metrics are clear.",
    dimension: "Value Case & Scope",
    isGating: false,
  },
  {
    id: "Q5",
    text: "Scope is defined and unlikely to change significantly.",
    dimension: "Value Case & Scope",
    isGating: false,
  },
  {
    id: "Q6",
    text: "Trade-offs (speed vs scope vs quality) are explicitly agreed.",
    dimension: "Value Case & Scope",
    isGating: false,
  },

  // C) Capacity & Roles
  {
    id: "Q7",
    text: "Key roles are named (process owner, data owner, change lead).",
    dimension: "Capacity & Roles",
    isGating: false,
  },
  {
    id: "Q8",
    text: 'People have dedicated time (not "on top of everything else").',
    dimension: "Capacity & Roles",
    isGating: true,
  },
  {
    id: "Q9",
    text: "Resourcing is realistic through go-live and hypercare.",
    dimension: "Capacity & Roles",
    isGating: false,
  },

  // D) Process & Governance
  {
    id: "Q10",
    text: "Target processes are documented and agreed.",
    dimension: "Process & Governance",
    isGating: false,
  },
  {
    id: "Q11",
    text: "Governance cadence exists (steerco, decisions, escalation path).",
    dimension: "Process & Governance",
    isGating: false,
  },
  {
    id: "Q12",
    text: "Change request management is defined (who decides, how, when).",
    dimension: "Process & Governance",
    isGating: false,
  },

  // E) Data & Tooling Readiness (Pigment)
  {
    id: "Q13",
    text: "Data sources are identified and accessible for Pigment.",
    dimension: "Data & Tooling Readiness",
    isGating: true,
  },
  {
    id: "Q14",
    text: "Data quality is sufficient OR a concrete remediation plan exists.",
    dimension: "Data & Tooling Readiness",
    isGating: false,
  },
  {
    id: "Q15",
    text: "Integrations/security/access (SSO/RBAC/ETL/API) are planned and testable in time.",
    dimension: "Data & Tooling Readiness",
    isGating: false,
  },
];

export const GATING_QUESTION_IDS = QUESTIONS.filter((q) => q.isGating).map(
  (q) => q.id
);
