"use client";

import { useState } from "react";
import { uploadDataset } from "@/lib/api";
import { DatasetUploadResponse } from "@/types/dataset";

export function useUpload() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] =
    useState<DatasetUploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function upload(file: File) {
    setLoading(true);
    setError(null);

    try {
      const response = await uploadDataset(file);

      setResult(response);

      return response;
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Upload failed";

      setError(message);

      throw err;
    } finally {
      setLoading(false);
    }
  }

  return {
    upload,
    loading,
    result,
    error,
  };
}