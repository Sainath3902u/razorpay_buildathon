
"use client";

import {
  ArrowUpRight,
} from "lucide-react";

import { Opportunity } from "@/types/opportunity";
import {
  capitalize,
  formatCurrency,
} from "@/lib/utils";

import { Badge } from "../ui/Badge";

interface Props {
  opportunities: Opportunity[];
  onSelect: (item: Opportunity) => void;
}

export function OpportunityTable({
  opportunities,
  onSelect,
}: Props) {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
      <div className="overflow-x-auto">
        <table className="w-full text-left">

          {/* Header */}
          <thead className="border-b border-slate-100 bg-slate-50">
            <tr>

              <th className="px-5 py-4 text-xs font-semibold text-slate-500">
                Opportunity
              </th>

              <th className="px-5 py-4 text-xs font-semibold text-slate-500">
                Category
              </th>

              <th className="px-5 py-4 text-xs font-semibold text-slate-500">
                Customer
              </th>

              <th className="px-5 py-4 text-xs font-semibold text-slate-500">
                At Risk
              </th>

              <th className="px-5 py-4 text-xs font-semibold text-slate-500">
                Expected
              </th>

              <th className="px-5 py-4 text-xs font-semibold text-slate-500">
                Priority
              </th>

            </tr>
          </thead>

          {/* Body */}
          <tbody className="divide-y divide-slate-100">

            {opportunities.map((item) => (

              <tr
                key={item.opportunity_id}
                onClick={() => onSelect(item)}
                className="cursor-pointer transition hover:bg-slate-50"
              >

                {/* Opportunity */}
                <td className="px-5 py-4">

                  <div className="flex items-center gap-3">

                    <div className="min-w-0 flex-1">

                      <p className="font-medium text-slate-900">
                        {capitalize(
                          item.opportunity_type
                        )}
                      </p>

                      <p className="mt-1 text-xs text-slate-400">
                        {item.opportunity_id}
                      </p>

                    </div>

                    {/* Explicit details button */}
                    <button
                      type="button"
                      onClick={(event) => {
                        event.stopPropagation();
                        onSelect(item);
                      }}
                      aria-label={`View details for ${item.opportunity_type}`}
                      title="View opportunity details"
                      className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-400 transition hover:border-[#146ef5] hover:bg-blue-50 hover:text-[#146ef5]"
                    >
                      <ArrowUpRight size={17} />
                    </button>

                  </div>

                </td>

                {/* Category */}
                <td className="px-5 py-4">
                  <Badge variant="blue">
                    {item.category}
                  </Badge>
                </td>

                {/* Customer */}
                <td className="px-5 py-4 text-sm text-slate-600">
                  {item.customer_id || "—"}
                </td>

                {/* At Risk */}
                <td className="px-5 py-4 font-semibold text-slate-900">
                  {formatCurrency(
                    item.amount_at_risk
                  )}
                </td>

                {/* Expected */}
                <td className="px-5 py-4 font-semibold text-emerald-600">
                  {formatCurrency(
                    item.expected_value
                  )}
                </td>

                {/* Priority */}
                <td className="px-5 py-4">

                  <Badge
                    variant={
                      item.priority === "HIGH"
                        ? "high"
                        : item.priority === "MEDIUM"
                          ? "medium"
                          : "low"
                    }
                  >
                    {item.priority}
                  </Badge>

                </td>

              </tr>

            ))}

          </tbody>

        </table>
      </div>

      {/* Empty state */}
      {opportunities.length === 0 && (
        <div className="p-12 text-center text-sm text-slate-400">
          No opportunities match your filters.
        </div>
      )}

    </div>
  );
}