"use client";

import { Opportunity } from "@/types/opportunity";

interface RevenueChartProps {
  opportunities: Opportunity[];
}

export function RevenueChart({
  opportunities,
}: RevenueChartProps) {
  /*
   * Use the real opportunities returned by FastAPI.
   *
   * We display the 12 highest expected-value opportunities.
   * This avoids showing fake historical/monthly data when the
   * backend does not currently provide monthly time-series data.
   */
  const chartData = [...opportunities]
    .sort(
      (a, b) =>
        b.expected_value - a.expected_value
    )
    .slice(0, 12);

  const maxValue =
    chartData.length > 0
      ? Math.max(
          ...chartData.map(
            (item) => item.expected_value
          )
        )
      : 0;

  const formatCurrency = (amount: number) => {
    if (!Number.isFinite(amount)) {
      return "₹0";
    }

    if (amount >= 10000000) {
      return `₹${(
        amount / 10000000
      ).toFixed(2)}Cr`;
    }

    if (amount >= 100000) {
      return `₹${(
        amount / 100000
      ).toFixed(2)}L`;
    }

    if (amount >= 1000) {
      return `₹${(
        amount / 1000
      ).toFixed(1)}K`;
    }

    return `₹${Math.round(
      amount
    ).toLocaleString("en-IN")}`;
  };

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm">

      {/* Header */}
      <div className="flex items-start justify-between">

        <div>
          <h2 className="text-lg font-semibold text-slate-950">
            Revenue exposure
          </h2>

          <p className="mt-1 text-sm text-slate-400">
            Highest-value opportunities detected
          </p>
        </div>

        <div className="rounded-lg border border-slate-200 px-4 py-2 text-sm text-slate-600">
          Top {chartData.length}
        </div>

      </div>

      {/* Chart */}
      {chartData.length === 0 ? (
        <div className="flex h-[320px] items-center justify-center">
          <div className="text-center">
            <p className="text-sm font-medium text-slate-600">
              No opportunities detected
            </p>

            <p className="mt-1 text-xs text-slate-400">
              Upload a dataset to populate this chart.
            </p>
          </div>
        </div>
      ) : (
        <div className="mt-8">

          <div className="flex h-[300px] items-end gap-3 overflow-hidden">

            {chartData.map(
              (opportunity, index) => {
                const height =
                  maxValue > 0
                    ? Math.max(
                        8,
                        (opportunity.expected_value /
                          maxValue) *
                          100
                      )
                    : 8;

                return (
                  <div
                    key={
                      opportunity.opportunity_id
                    }
                    className="flex h-full flex-1 flex-col justify-end"
                  >

                    <div className="group relative flex h-full items-end">

                      {/* Tooltip */}
                      <div className="pointer-events-none absolute bottom-full left-1/2 z-10 mb-2 hidden -translate-x-1/2 whitespace-nowrap rounded-lg bg-slate-900 px-3 py-2 text-xs text-white shadow-lg group-hover:block">
                        <div className="font-medium">
                          {
                            opportunity.opportunity_type
                          }
                        </div>

                        <div className="mt-1">
                          Expected value:{" "}
                          {formatCurrency(
                            opportunity.expected_value
                          )}
                        </div>
                      </div>

                      {/* Bar */}
                      <div
                        className="w-full rounded-t-lg bg-[#4389ed] transition-all duration-300 hover:opacity-80"
                        style={{
                          height: `${height}%`,
                        }}
                      />
                    </div>

                    {/* Label */}
                    <div className="mt-3 truncate text-center text-[11px] text-slate-400">
                      {index + 1}
                    </div>

                  </div>
                );
              }
            )}

          </div>

          <div className="mt-4 flex justify-between text-xs text-slate-400">
            <span>
              Highest value
            </span>

            <span>
              Lowest value
            </span>
          </div>

        </div>
      )}

    </div>
  );
}