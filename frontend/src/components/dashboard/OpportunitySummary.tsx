"use client";

import { Card } from "../ui/Card";

import { Opportunity } from "@/types/opportunity";
import { AnalysisSummary } from "@/lib/api";

interface OpportunitySummaryProps {
  summary: AnalysisSummary | null;
  opportunities: Opportunity[];
}

export function OpportunitySummary({
  summary,
  opportunities,
}: OpportunitySummaryProps) {
  /*
   * Get category counts from the backend summary.
   *
   * Fallback to calculating them from opportunities
   * in case the backend summary is missing.
   */

  const recover =
    summary?.category_counts?.RECOVER ??
    opportunities.filter(
      (opportunity) =>
        opportunity.category === "RECOVER"
    ).length;

  const prevent =
    summary?.category_counts?.PREVENT ??
    opportunities.filter(
      (opportunity) =>
        opportunity.category === "PREVENT"
    ).length;

  const grow =
    summary?.category_counts?.GROW ??
    opportunities.filter(
      (opportunity) =>
        opportunity.category === "GROW"
    ).length;

  const total =
    recover +
    prevent +
    grow;

  /*
   * Calculate percentages from REAL data.
   */

  const recoverPercentage =
    total > 0
      ? (recover / total) * 100
      : 0;

  const preventPercentage =
    total > 0
      ? (prevent / total) * 100
      : 0;

  const growPercentage =
    total > 0
      ? (grow / total) * 100
      : 0;

  const data = [
    {
      label: "Recover",
      value: recover,
      percentage: recoverPercentage,
      className: "bg-blue-500",
    },
    {
      label: "Prevent",
      value: prevent,
      percentage: preventPercentage,
      className: "bg-violet-500",
    },
    {
      label: "Grow",
      value: grow,
      percentage: growPercentage,
      className: "bg-emerald-500",
    },
  ];

  return (
    <Card className="p-6">

      {/* Header */}
      <div>
        <h2 className="font-semibold text-slate-950">
          Opportunity mix
        </h2>

        <p className="mt-1 text-xs text-slate-400">
          Distribution across revenue actions
        </p>
      </div>

      {/* No opportunities */}
      {total === 0 ? (
        <div className="flex min-h-[220px] items-center justify-center text-center">
          <div>
            <p className="text-sm font-medium text-slate-600">
              No opportunities detected
            </p>

            <p className="mt-1 text-xs text-slate-400">
              Upload a dataset to see the opportunity mix.
            </p>
          </div>
        </div>
      ) : (
        <div className="mt-6 space-y-5">

          {data.map((item) => (
            <div key={item.label}>

              {/* Label + count */}
              <div className="mb-2 flex justify-between text-sm">

                <span className="font-medium text-slate-700">
                  {item.label}
                </span>

                <span className="font-semibold text-slate-950">
                  {item.value}
                </span>

              </div>

              {/* Progress bar */}
              <div className="h-2 overflow-hidden rounded-full bg-slate-100">

                <div
                  className={`h-full rounded-full ${item.className}`}
                  style={{
                    width: `${item.percentage}%`,
                  }}
                />

              </div>

              {/* Percentage */}
              <div className="mt-1 text-right text-[11px] text-slate-400">
                {item.percentage.toFixed(1)}%
              </div>

            </div>
          ))}

        </div>
      )}

    </Card>
  );
}