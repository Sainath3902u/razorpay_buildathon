export interface DatasetUploadResponse {
  success: boolean;

  dataset_id: string;

  filename: string;

  rows: number;

  columns: number;

  capabilities:
    | Record<string, boolean>
    | string[]
    | null;

  column_mapping:
    | Record<string, string>
    | null;

  normalized_file?: string;
}


export interface DatasetState {

  datasetId: string | null;

  filename: string | null;

  rows: number;

  columns: number;

  capabilities: string[];

  columnMapping: Record<string, string>;

  summary?: {
    total_opportunities: number;

    total_amount_at_risk: number;

    total_expected_value: number;

    category_counts: {
      RECOVER: number;
      PREVENT: number;
      GROW: number;
    };

    priority_counts: {
      HIGH: number;
      MEDIUM: number;
      LOW: number;
    };
  };
}