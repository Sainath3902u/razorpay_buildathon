"use client";

import { useEffect, useState } from "react";
import { getOpportunities } from "@/lib/api";
import { Opportunity } from "@/types/opportunity";

export function useOpportunities(
  datasetId?: string | null
) {
  const [opportunities, setOpportunities] =
    useState<Opportunity[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    if (!datasetId) return;

    const currentDatasetId = datasetId;

    let active = true;

    async function load() {
      setLoading(true);
      setError(null);

      try {
        const data =
          await getOpportunities(currentDatasetId);

        if (active) {
          setOpportunities(data);
        }
      } catch (err) {
        if (active) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load opportunities"
          );
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    load();

    return () => {
      active = false;
    };
  }, [datasetId]);

  return {
    opportunities,
    loading,
    error,
  };
}