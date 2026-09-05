"use client";

import {
  User,
  Hash,
  Cpu,
  ShieldCheck,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";

import { Opportunity } from "@/types/opportunity";

interface OpportunityDetailsProps {
  opportunity: Opportunity | null;
}

export function OpportunityDetails({
  opportunity,
}: OpportunityDetailsProps) {
  if (!opportunity) {
    return null;
  }

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

  const probability =
    opportunity.probability <= 1
      ? opportunity.probability * 100
      : opportunity.probability;

  const safeProbability = Math.min(
    100,
    Math.max(0, probability)
  );

  return (
    <div className="space-y-7">

      {/* Status */}
      <div className="flex flex-wrap gap-2">

        <span
          className={`rounded-full px-3 py-1 text-xs font-semibold ${
            opportunity.priority === "HIGH"
              ? "bg-red-50 text-red-600"
              : opportunity.priority === "MEDIUM"
                ? "bg-amber-50 text-amber-600"
                : "bg-slate-100 text-slate-600"
          }`}
        >
          {opportunity.priority}
        </span>

        <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-600">
          {opportunity.category}
        </span>

      </div>

      {/* Opportunity name */}
      <div>

        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
          Opportunity
        </p>

        <h1 className="mt-2 text-2xl font-bold tracking-tight text-slate-950">
          {opportunity.opportunity_type}
        </h1>

      </div>

      {/* Financial values */}
      <div className="grid gap-4 md:grid-cols-2">

        <div className="rounded-xl bg-slate-50 p-5">

          <p className="text-sm text-slate-400">
            Amount at risk
          </p>

          <p className="mt-2 text-2xl font-bold text-slate-950">
            {formatCurrency(
              opportunity.amount_at_risk
            )}
          </p>

        </div>

        <div className="rounded-xl bg-emerald-50 p-5">

          <p className="text-sm text-emerald-600">
            Expected value
          </p>

          <p className="mt-2 text-2xl font-bold text-emerald-700">
            {formatCurrency(
              opportunity.expected_value
            )}
          </p>

        </div>

      </div>

      {/* Opportunity information */}
      <div>

        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
          Opportunity information
        </h3>

        <div className="mt-4 grid gap-3 md:grid-cols-2">

          {/* Opportunity ID */}
          <div className="flex items-center gap-3 rounded-xl border border-slate-100 p-4">

            <Hash className="h-5 w-5 shrink-0 text-slate-400" />

            <div className="min-w-0">

              <p className="text-xs text-slate-400">
                Opportunity ID
              </p>

              <p className="mt-1 truncate text-sm font-medium text-slate-800">
                {opportunity.opportunity_id}
              </p>

            </div>

          </div>

          {/* Customer */}
          <div className="flex items-center gap-3 rounded-xl border border-slate-100 p-4">

            <User className="h-5 w-5 shrink-0 text-slate-400" />

            <div className="min-w-0">

              <p className="text-xs text-slate-400">
                Customer ID
              </p>

              <p className="mt-1 truncate text-sm font-medium text-slate-800">
                {opportunity.customer_id ||
                  "Not available"}
              </p>

            </div>

          </div>

          {/* Source detector */}
          <div className="flex items-center gap-3 rounded-xl border border-slate-100 p-4">

            <Cpu className="h-5 w-5 shrink-0 text-slate-400" />

            <div className="min-w-0">

              <p className="text-xs text-slate-400">
                Source detector
              </p>

              <p className="mt-1 truncate text-sm font-medium text-slate-800">
                {opportunity.source_detector ||
                  "Revenue intelligence engine"}
              </p>

            </div>

          </div>

          {/* Revenue action */}
          <div className="flex items-center gap-3 rounded-xl border border-slate-100 p-4">

            <ShieldCheck className="h-5 w-5 shrink-0 text-slate-400" />

            <div className="min-w-0">

              <p className="text-xs text-slate-400">
                Revenue action
              </p>

              <p className="mt-1 truncate text-sm font-medium text-slate-800">
                {opportunity.category}
              </p>

            </div>

          </div>

        </div>

      </div>

      {/* Why detected */}
      <div>

        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
          Why this was detected
        </h3>

        <div className="mt-3 rounded-xl bg-slate-50 p-5">

          <div className="flex gap-3">

            <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-amber-500" />

            <p className="text-sm leading-6 text-slate-600">
              {opportunity.reason ||
                "The revenue intelligence engine identified this opportunity from the uploaded dataset."}
            </p>

          </div>

        </div>

      </div>

      {/* Recommended action */}
      <div>

        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
          Recommended action
        </h3>

        <div className="mt-3 rounded-xl bg-blue-50 p-5">

          <p className="text-sm font-semibold leading-6 text-blue-700">
            {opportunity.recommended_action ||
              "Review and take the recommended revenue action."}
          </p>

        </div>

      </div>

      {/* Recovery eligibility */}
      <div>

        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
          Recovery eligibility
        </h3>

        <div
          className={`mt-3 rounded-xl p-5 ${
            opportunity.recovery_eligible
              ? "bg-emerald-50"
              : "bg-slate-50"
          }`}
        >

          <div className="flex items-start gap-3">

            {opportunity.recovery_eligible ? (
              <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-emerald-600" />
            ) : (
              <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-slate-400" />
            )}

            <div>

              <p
                className={`text-sm font-semibold ${
                  opportunity.recovery_eligible
                    ? "text-emerald-700"
                    : "text-slate-600"
                }`}
              >
                {opportunity.recovery_eligible
                  ? "Eligible for recovery"
                  : "Recovery not confirmed"}
              </p>

              {opportunity.recovery_reason && (
                <p className="mt-1 text-sm leading-5 text-slate-500">
                  {opportunity.recovery_reason}
                </p>
              )}

            </div>

          </div>

        </div>

      </div>

      {/* Probability */}
      <div>

        <div className="flex items-center justify-between">

          <h3 className="text-sm font-medium text-slate-500">
            Recovery probability
          </h3>

          <span className="text-sm font-bold text-slate-900">
            {safeProbability.toFixed(0)}%
          </span>

        </div>

        <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">

          <div
            className="h-full rounded-full bg-blue-500 transition-all duration-500"
            style={{
              width: `${safeProbability}%`,
            }}
          />

        </div>

      </div>

    </div>
  );
}