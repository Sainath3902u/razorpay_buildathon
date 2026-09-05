export type OpportunityCategory =
  | "RECOVER"
  | "PREVENT"
  | "GROW";

export type Priority =
  | "HIGH"
  | "MEDIUM"
  | "LOW";

export interface Opportunity {
  opportunity_id: string;
  category: OpportunityCategory;
  opportunity_type: string;
  customer_id?: string | null;

  amount_at_risk: number;
  probability: number;
  expected_value: number;

  reason: string;
  recommended_action: string;

  priority: Priority;

  recovery_eligible?: boolean;
  recovery_reason?: string;

  source_detector?: string;
}