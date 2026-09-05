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

          <tbody className="divide-y divide-slate-100">
            {opportunities.map((item) => (
              <tr
                key={item.opportunity_id}
                onClick={() => onSelect(item)}
                className="cursor-pointer hover:bg-slate-50"
              >
                <td className="px-5 py-4">
                  <p className="font-medium text-slate-900">
                    {capitalize(
                      item.opportunity_type
                    )}
                  </p>

                  <p className="mt-1 text-xs text-slate-400">
                    {item.opportunity_id}
                  </p>
                </td>

                <td className="px-5 py-4">
                  <Badge variant="blue">
                    {item.category}
                  </Badge>
                </td>

                <td className="px-5 py-4 text-sm text-slate-600">
                  {item.customer_id || "—"}
                </td>

                <td className="px-5 py-4 font-semibold text-slate-900">
                  {formatCurrency(
                    item.amount_at_risk
                  )}
                </td>

                <td className="px-5 py-4 font-semibold text-emerald-600">
                  {formatCurrency(
                    item.expected_value
                  )}
                </td>

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

      {opportunities.length === 0 && (
        <div className="p-12 text-center text-sm text-slate-400">
          No opportunities match your filters.
        </div>
      )}
    </div>
  );
}