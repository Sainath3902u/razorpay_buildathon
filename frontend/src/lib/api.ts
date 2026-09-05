import { API_BASE_URL } from "@/config/env";
import { DatasetUploadResponse } from "@/types/dataset";
import { Opportunity } from "@/types/opportunity";

async function parseResponse<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const message =
      data?.detail ||
      data?.message ||
      "Something went wrong";

    throw new Error(message);
  }

  return data as T;
}

export async function uploadDataset(
  file: File
): Promise<DatasetUploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  return parseResponse<DatasetUploadResponse>(response);
}

export async function checkHealth() {
  const response = await fetch(
    `${API_BASE_URL}/health`,
    {
      cache: "no-store",
    }
  );

  return parseResponse<{ status: string }>(response);
}

/*
 * This endpoint can be enabled after adding
 * /api/opportunities or /api/analyze to FastAPI.
 */
export async function getOpportunities(
  datasetId: string
): Promise<Opportunity[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/opportunities/${datasetId}`,
    {
      cache: "no-store",
    }
  );

  const data =
    await parseResponse<{
      opportunities: Opportunity[];
    }>(response);

  return data.opportunities;
}