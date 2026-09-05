"use client";

import Link from "next/link";

import {
  ArrowUpRight,
  AlertCircle,
} from "lucide-react";

import { Opportunity } from "@/types/opportunity";

interface RecentOpportunitiesProps {
  opportunities: Opportunity[];
}

export function RecentOpportunities({
  opportunities,
}: RecentOpportunitiesProps) {
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

  /*
   * Show highest-value real opportunities first.
   */
  const recentOpportunities = [
    ...opportunities,
  ]
    .sort(
      (a, b) =>
        b.expected_value -
        a.expected_value
    )
    .slice(0, 5);

  const priorityClass = (
    priority: string
  ) => {
    switch (priority) {
      case "HIGH":
        return "bg-red-50 text-red-600";

      case "MEDIUM":
        return "bg-amber-50 text-amber-600";

      default:
        return "bg-slate-100 text-slate-600";
    }
  };

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">

      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-100 px-7 py-6">

        <div>
          <h2 className="text-lg font-semibold text-slate-950">
            Highest-value opportunities
          </h2>

          <p className="mt-1 text-sm text-slate-400">
            Revenue actions worth prioritising
          </p>
        </div>

        <Link
          href="/opportunities"
          className="text-sm font-semibold text-[#146ef5] hover:underline"
        >
          View all
        </Link>

      </div>

      {/* Empty state */}
      {recentOpportunities.length === 0 ? (
        <div className="px-7 py-12 text-center">

          <AlertCircle className="mx-auto h-8 w-8 text-slate-300" />

          <p className="mt-3 text-sm font-medium text-slate-600">
            No opportunities detected
          </p>

          <p className="mt-1 text-xs text-slate-400">
            Upload a dataset to see revenue opportunities.
          </p>

        </div>
      ) : (
        <div>
          {recentOpportunities.map(
            (opportunity) => (
              <div
                key={
                  opportunity.opportunity_id
                }
                className="flex items-center justify-between border-b border-slate-100 px-7 py-5 last:border-b-0"
              >

                {/* Left */}
                <div className="min-w-0">

                  <div className="flex items-center gap-3">

                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${priorityClass(
                        opportunity.priority
                      )}`}
                    >
                      {opportunity.priority}
                    </span>

                    <h3 className="truncate text-sm font-medium text-slate-900">
                      {opportunity.opportunity_type}
                    </h3>

                  </div>

                  <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-slate-400">

                    {opportunity.customer_id && (
                      <span>
                        {opportunity.customer_id}
                      </span>
                    )}

                    <span>
                      {opportunity.opportunity_id}
                    </span>

                  </div>

                </div>

                {/* Right */}
                <div className="ml-6 flex shrink-0 items-center gap-5">

                  <div className="text-right">

                    <div className="text-sm font-semibold text-slate-900">
                      {formatCurrency(
                        opportunity.expected_value
                      )}
                    </div>

                    <div className="mt-1 text-xs text-slate-400">
                      Expected value
                    </div>

                  </div>

                  <ArrowUpRight className="h-5 w-5 text-slate-400" />

                </div>

              </div>
            )
          )}
        </div>
      )}

    </div>
  );
}