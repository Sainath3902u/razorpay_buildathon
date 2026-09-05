"use client";

import { useEffect, useState } from "react";
import { DatasetState } from "@/types/dataset";

const STORAGE_KEY = "revenue-intelligence-dataset";

export function useDataset() {
  const [dataset, setDataset] =
    useState<DatasetState | null>(null);

  useEffect(() => {
    let active = true;

    queueMicrotask(() => {
      const saved = localStorage.getItem(STORAGE_KEY);

      if (!active || !saved) return;

      try {
        setDataset(JSON.parse(saved));
      } catch {
        localStorage.removeItem(STORAGE_KEY);
      }
    });

    return () => {
      active = false;
    };
  }, []);

  function saveDataset(data: DatasetState) {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(data)
    );

    setDataset(data);
  }

  function clearDataset() {
    localStorage.removeItem(STORAGE_KEY);
    setDataset(null);
  }

  return {
    dataset,
    saveDataset,
    clearDataset,
  };
}