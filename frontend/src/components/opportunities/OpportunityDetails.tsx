// import { Opportunity } from "@/types/opportunity";
// import { Badge } from "../ui/Badge";
// import { formatCurrency, formatPercentage } from "@/lib/utils";

// interface Props {
//   opportunity: Opportunity;
// }

// export function OpportunityDetails({
//   opportunity,
// }: Props) {
//   return (
//     <div className="space-y-5">
//       <div className="flex gap-2">
//         <Badge
//           variant={
//             opportunity.priority === "HIGH"
//               ? "high"
//               : opportunity.priority === "MEDIUM"
//                 ? "medium"
//                 : "low"
//           }
//         >
//           {opportunity.priority}
//         </Badge>

//         <Badge variant="blue">
//           {opportunity.category}
//         </Badge>
//       </div>

//       <div>
//         <p className="text-xs text-slate-400">
//           Opportunity
//         </p>

//         <h3 className="mt-1 text-xl font-bold text-slate-950">
//           {opportunity.opportunity_type}
//         </h3>
//       </div>

//       <div className="grid grid-cols-2 gap-3">
//         <div className="rounded-xl bg-slate-50 p-4">
//           <p className="text-xs text-slate-400">
//             Amount at risk
//           </p>

//           <p className="mt-1 font-bold">
//             {formatCurrency(
//               opportunity.amount_at_risk
//             )}
//           </p>
//         </div>

//         <div className="rounded-xl bg-emerald-50 p-4">
//           <p className="text-xs text-emerald-600">
//             Expected value
//           </p>

//           <p className="mt-1 font-bold text-emerald-700">
//             {formatCurrency(
//               opportunity.expected_value
//             )}
//           </p>
//         </div>
//       </div>

//       <div>
//         <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
//           Why this was detected
//         </p>

//         <p className="mt-2 text-sm leading-6 text-slate-600">
//           {opportunity.reason ||
//             "The intelligence engine identified this as a revenue opportunity."}
//         </p>
//       </div>

//       <div>
//         <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
//           Recommended action
//         </p>

//         <div className="mt-2 rounded-xl bg-blue-50 p-4 text-sm font-medium leading-6 text-blue-800">
//           {opportunity.recommended_action ||
//             "Prioritize this opportunity for review."}
//         </div>
//       </div>

//       <div>
//         <div className="mb-2 flex justify-between text-xs">
//           <span className="text-slate-400">
//             Recovery probability
//           </span>

//           <span className="font-semibold">
//             {formatPercentage(
//               opportunity.probability
//             )}
//           </span>
//         </div>

//         <div className="h-2 rounded-full bg-slate-100">
//           <div
//             className="h-full rounded-full bg-[#146ef5]"
//             style={{
//               width: `${opportunity.probability * 100}%`,
//             }}
//           />
//         </div>
//       </div>
//     </div>
//   );
// }


"use client";

import {
  X,
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
  onClose: () => void;
}

export function OpportunityDetails({
  opportunity,
  onClose,
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

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">

      <div className="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-2xl bg-white shadow-2xl">

        {/* Header */}
        <div className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white px-6 py-5">

          <h2 className="text-lg font-semibold text-slate-900">
            Opportunity details
          </h2>

          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
          >
            <X className="h-5 w-5" />
          </button>

        </div>

        <div className="space-y-7 p-6">

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

          {/* Basic information */}
          <div>

            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
              Opportunity information
            </h3>

            <div className="mt-4 grid gap-3 md:grid-cols-2">

              {/* Opportunity ID */}
              <div className="flex items-center gap-3 rounded-xl border border-slate-100 p-4">

                <Hash className="h-5 w-5 text-slate-400" />

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

                <User className="h-5 w-5 text-slate-400" />

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

              {/* Detector */}
              <div className="flex items-center gap-3 rounded-xl border border-slate-100 p-4">

                <Cpu className="h-5 w-5 text-slate-400" />

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

              {/* Category */}
              <div className="flex items-center gap-3 rounded-xl border border-slate-100 p-4">

                <ShieldCheck className="h-5 w-5 text-slate-400" />

                <div>

                  <p className="text-xs text-slate-400">
                    Revenue action
                  </p>

                  <p className="mt-1 text-sm font-medium text-slate-800">
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

              <p className="text-sm font-semibold text-blue-700">
                {opportunity.recommended_action ||
                  "Review and take appropriate revenue action."}
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
                {probability.toFixed(0)}%
              </span>

            </div>

            <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">

              <div
                className="h-full rounded-full bg-blue-500 transition-all"
                style={{
                  width: `${Math.min(
                    100,
                    Math.max(0, probability)
                  )}%`,
                }}
              />

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}