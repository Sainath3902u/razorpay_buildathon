import {
  ArrowUpRight,
  ShieldAlert,
  TrendingUp,
  RotateCcw,
} from "lucide-react";

import { Opportunity } from "@/types/opportunity";
import { Badge } from "../ui/Badge";
import { Card } from "../ui/Card";
import {
  capitalize,
  formatCurrency,
  formatPercentage,
} from "@/lib/utils";

interface OpportunityCardProps {
  opportunity: Opportunity;
  onClick?: () => void;
}

export function OpportunityCard({
  opportunity,
  onClick,
}: OpportunityCardProps) {
  const icon =
    opportunity.category === "RECOVER"
      ? RotateCcw
      : opportunity.category === "PREVENT"
        ? ShieldAlert
        : TrendingUp;

  const Icon = icon;

  const badgeVariant =
    opportunity.priority === "HIGH"
      ? "high"
      : opportunity.priority === "MEDIUM"
        ? "medium"
        : "low";

  return (
    <Card
      className="cursor-pointer p-5 transition hover:-translate-y-0.5 hover:shadow-md"
      onClick={onClick}
    >
      <div className="flex items-start justify-between">
        <div className="flex gap-3">
          <div className="rounded-xl bg-slate-100 p-3 text-slate-600">
            <Icon size={19} />
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant={badgeVariant}>
                {opportunity.priority}
              </Badge>

              <Badge variant="blue">
                {opportunity.category}
              </Badge>
            </div>

            <h3 className="mt-2 font-semibold text-slate-950">
              {capitalize(
                opportunity.opportunity_type
              )}
            </h3>

            {opportunity.customer_id && (
              <p className="mt-1 text-xs text-slate-400">
                Customer {opportunity.customer_id}
              </p>
            )}
          </div>
        </div>

        <ArrowUpRight
          size={18}
          className="text-slate-400"
        />
      </div>

      <div className="mt-5 grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-slate-400">
            At risk
          </p>

          <p className="mt-1 font-bold text-slate-950">
            {formatCurrency(
              opportunity.amount_at_risk
            )}
          </p>
        </div>

        <div>
          <p className="text-xs text-slate-400">
            Expected value
          </p>

          <p className="mt-1 font-bold text-emerald-600">
            {formatCurrency(
              opportunity.expected_value
            )}
          </p>
        </div>
      </div>

      <div className="mt-4">
        <div className="mb-1 flex justify-between text-xs">
          <span className="text-slate-400">
            Success probability
          </span>

          <span className="font-semibold text-slate-700">
            {formatPercentage(
              opportunity.probability
            )}
          </span>
        </div>

        <div className="h-1.5 overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-[#146ef5]"
            style={{
              width: `${opportunity.probability * 100}%`,
            }}
          />
        </div>
      </div>
    </Card>
  );
}