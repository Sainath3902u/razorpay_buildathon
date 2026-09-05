export interface DatasetUploadResponse {
  success: boolean;
  dataset_id: string;
  filename: string;
  rows: number;
  columns: number;
  capabilities: Record<string, unknown> | string[] | null;
  column_mapping: Record<string, string> | null;
  normalized_file?: string;
}

export interface DatasetState {
  datasetId: string | null;
  filename: string | null;
  rows: number;
  columns: number;
  capabilities: string[];
  columnMapping: Record<string, string>;
}