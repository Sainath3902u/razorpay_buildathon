"use client";

import { useEffect, useState } from "react";

import {
  getOpportunities,
  AnalysisSummary,
} from "@/lib/api";

import {
  Opportunity,
} from "@/types/opportunity";


export function useOpportunities(
  datasetId?: string | null
) {

  const [
    opportunities,
    setOpportunities,
  ] = useState<Opportunity[]>([]);

  const [
    summary,
    setSummary,
  ] = useState<AnalysisSummary | null>(null);

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<string | null>(null);


  useEffect(() => {

    // No dataset selected
    if (!datasetId) {

      setOpportunities([]);
      setSummary(null);
      setError(null);
      setLoading(false);

      return;
    }

    // At this point datasetId is definitely a string.
    const id = datasetId;

    let active = true;


    async function load() {

      setLoading(true);
      setError(null);

      try {

        const data = await getOpportunities(id);

        if (!active) {
          return;
        }

        setOpportunities(
          data.opportunities
        );

        setSummary(
          data.summary
        );

      } catch (err) {

        if (!active) {
          return;
        }

        setError(
          err instanceof Error
            ? err.message
            : "Unable to load opportunities"
        );

        setOpportunities([]);
        setSummary(null);

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
    summary,
    loading,
    error,
  };
}