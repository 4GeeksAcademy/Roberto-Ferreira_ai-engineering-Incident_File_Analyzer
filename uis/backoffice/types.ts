export type Breakdown = Record<string, number>;

export type AnalysisSummary = {
  total_records: number;
  valid_records: number;
  invalid_records: number;
  invalid_details: Array<{ row_number: number; reasons: string[] }>;
  invalid_by_reason: Breakdown;
  category_breakdown: Breakdown;
  status_breakdown: Breakdown;
  average_satisfaction: number | null;
  satisfaction_sample_size: number;
  satisfaction_distribution: Breakdown;
};
