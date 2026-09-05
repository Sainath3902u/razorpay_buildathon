import { DatasetUploadResponse } from "./dataset";
import { Opportunity } from "./opportunity";

export interface ApiError {
  detail?: string;
  message?: string;
}

export interface OpportunitiesResponse {
  success: boolean;
  opportunities: Opportunity[];
}

export type UploadResult = DatasetUploadResponse;