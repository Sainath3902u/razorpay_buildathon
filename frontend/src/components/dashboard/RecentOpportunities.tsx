import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Card } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { formatCurrency } from "@/lib/utils";

const opportunities = [
  {
    id: "CHK-DROP-104",
    type: "Checkout Drop-off",
    customer: "CUST-104",
    value: 420000,
    priority: "HIGH",
  },
  {
    id: "PREVENT-CHURN-221",
    type: "Churn Risk",
    customer: "CUST-221",
    value: 210000,
    priority: "MEDIUM",
  },
  {
    id: "SUB-FAIL-309",
    type: "Failed Subscription",
    customer: "CUST-309",
    value: 175000,
    priority: "HIGH",
  },
];

export function RecentOpportunities() {
  return (
    <Card className="overflow-hidden">
      <div className="flex items-center justify-between border-b border-slate-100 p-6">
        <div>
          <h2 className="font-semibold text-slate-950">
            Highest-value opportunities
          </h2>

          <p className="mt-1 text-xs text-slate-400">
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

      <div className="divide-y divide-slate-100">
        {opportunities.map((item) => (
          <div
            key={item.id}
            className="flex items-center justify-between p-5"
          >
            <div>
              <div className="flex items-center gap-3">
                <Badge
                  variant={
                    item.priority === "HIGH"
                      ? "high"
                      : "medium"
                  }
                >
                  {item.priority}
                </Badge>

                <span className="font-medium text-slate-900">
                  {item.type}
                </span>
              </div>

              <p className="mt-2 text-xs text-slate-400">
                {item.customer}
              </p>
            </div>

            <div className="flex items-center gap-5">
              <span className="font-bold text-slate-950">
                {formatCurrency(item.value)}
              </span>

              <button className="rounded-lg p-2 text-slate-400 hover:bg-slate-100">
                <ArrowUpRight size={18} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}