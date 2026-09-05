import { API_BASE_URL } from "@/config/env";
import {
  DatasetUploadResponse,
} from "@/types/dataset";
import {
  Opportunity,
} from "@/types/opportunity";

export interface AnalysisSummary {
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
}

export interface AnalysisResponse
  extends DatasetUploadResponse {
  summary: AnalysisSummary;
  opportunities: Opportunity[];
}


async function parseResponse<T>(
  response: Response
): Promise<T> {

  const data = await response
    .json()
    .catch(() => null);

  if (!response.ok) {

    const message =
      data?.detail ||
      data?.message ||
      `Request failed with status ${response.status}`;

    throw new Error(message);
  }

  return data as T;
}


export async function uploadDataset(
  file: File
): Promise<AnalysisResponse> {

  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  let response: Response;

  try {

    response = await fetch(
      `${API_BASE_URL}/api/upload`,
      {
        method: "POST",
        body: formData,
      }
    );

  } catch (error) {

    throw new Error(
      "Cannot connect to FastAPI. Make sure the backend is running on http://localhost:8000."
    );
  }

  return parseResponse<AnalysisResponse>(
    response
  );
}


export async function getOpportunities(
  datasetId: string
): Promise<AnalysisResponse> {

  let response: Response;

  try {

    response = await fetch(
      `${API_BASE_URL}/api/opportunities/${datasetId}`,
      {
        method: "GET",
        cache: "no-store",
      }
    );

  } catch (error) {

    throw new Error(
      "Cannot connect to FastAPI. Make sure the backend is running on http://localhost:8000."
    );
  }

  return parseResponse<AnalysisResponse>(
    response
  );
}


export async function checkHealth() {

  const response = await fetch(
    `${API_BASE_URL}/health`,
    {
      cache: "no-store",
    }
  );

  return parseResponse<{
    status: string;
  }>(response);
}