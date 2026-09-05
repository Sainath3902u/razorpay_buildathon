import { Opportunity } from "@/types/opportunity";
import { Badge } from "../ui/Badge";
import { formatCurrency, formatPercentage } from "@/lib/utils";

interface Props {
  opportunity: Opportunity;
}

export function OpportunityDetails({
  opportunity,
}: Props) {
  return (
    <div className="space-y-5">
      <div className="flex gap-2">
        <Badge
          variant={
            opportunity.priority === "HIGH"
              ? "high"
              : opportunity.priority === "MEDIUM"
                ? "medium"
                : "low"
          }
        >
          {opportunity.priority}
        </Badge>

        <Badge variant="blue">
          {opportunity.category}
        </Badge>
      </div>

      <div>
        <p className="text-xs text-slate-400">
          Opportunity
        </p>

        <h3 className="mt-1 text-xl font-bold text-slate-950">
          {opportunity.opportunity_type}
        </h3>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-xl bg-slate-50 p-4">
          <p className="text-xs text-slate-400">
            Amount at risk
          </p>

          <p className="mt-1 font-bold">
            {formatCurrency(
              opportunity.amount_at_risk
            )}
          </p>
        </div>

        <div className="rounded-xl bg-emerald-50 p-4">
          <p className="text-xs text-emerald-600">
            Expected value
          </p>

          <p className="mt-1 font-bold text-emerald-700">
            {formatCurrency(
              opportunity.expected_value
            )}
          </p>
        </div>
      </div>

      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
          Why this was detected
        </p>

        <p className="mt-2 text-sm leading-6 text-slate-600">
          {opportunity.reason ||
            "The intelligence engine identified this as a revenue opportunity."}
        </p>
      </div>

      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
          Recommended action
        </p>

        <div className="mt-2 rounded-xl bg-blue-50 p-4 text-sm font-medium leading-6 text-blue-800">
          {opportunity.recommended_action ||
            "Prioritize this opportunity for review."}
        </div>
      </div>

      <div>
        <div className="mb-2 flex justify-between text-xs">
          <span className="text-slate-400">
            Recovery probability
          </span>

          <span className="font-semibold">
            {formatPercentage(
              opportunity.probability
            )}
          </span>
        </div>

        <div className="h-2 rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-[#146ef5]"
            style={{
              width: `${opportunity.probability * 100}%`,
            }}
          />
        </div>
      </div>
    </div>
  );
}