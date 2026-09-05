import {
  CheckCircle2,
  Database,
  Columns3,
  Rows3,
} from "lucide-react";
import { Card } from "../ui/Card";
import { Button } from "../ui/Button";
import { DatasetUploadResponse } from "@/types/dataset";
import { formatNumber } from "@/lib/utils";

interface DatasetSummaryProps {
  result: DatasetUploadResponse;
  onContinue: () => void;
}

export function DatasetSummary({
  result,
  onContinue,
}: DatasetSummaryProps) {
  const capabilities = Array.isArray(
    result.capabilities
  )
    ? result.capabilities
    : Object.keys(result.capabilities || {});

  return (
    <Card className="mt-8 overflow-hidden">
      <div className="border-b border-slate-100 bg-emerald-50/50 p-6">
        <div className="flex items-center gap-3">
          <CheckCircle2
            className="text-emerald-600"
            size={24}
          />

          <div>
            <h2 className="font-semibold text-slate-950">
              Dataset analyzed successfully
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              {result.filename}
            </p>
          </div>
        </div>
      </div>

      <div className="grid gap-4 p-6 sm:grid-cols-3">
        <div className="rounded-xl bg-slate-50 p-4">
          <Rows3
            size={18}
            className="text-[#146ef5]"
          />

          <p className="mt-3 text-2xl font-bold text-slate-950">
            {formatNumber(result.rows)}
          </p>

          <p className="text-xs text-slate-400">
            Rows
          </p>
        </div>

        <div className="rounded-xl bg-slate-50 p-4">
          <Columns3
            size={18}
            className="text-[#146ef5]"
          />

          <p className="mt-3 text-2xl font-bold text-slate-950">
            {result.columns}
          </p>

          <p className="text-xs text-slate-400">
            Columns
          </p>
        </div>

        <div className="rounded-xl bg-slate-50 p-4">
          <Database
            size={18}
            className="text-[#146ef5]"
          />

          <p className="mt-3 text-2xl font-bold text-slate-950">
            {capabilities.length}
          </p>

          <p className="text-xs text-slate-400">
            Capabilities
          </p>
        </div>
      </div>

      {capabilities.length > 0 && (
        <div className="border-t border-slate-100 p-6">
          <p className="mb-3 text-sm font-semibold text-slate-900">
            Detected capabilities
          </p>

          <div className="flex flex-wrap gap-2">
            {capabilities.map((item) => (
              <span
                key={item}
                className="rounded-full bg-blue-50 px-3 py-1.5 text-xs font-semibold text-blue-700"
              >
                ✓ {item}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="flex justify-end border-t border-slate-100 p-6">
        <Button onClick={onContinue}>
          View Dashboard →
        </Button>
      </div>
    </Card>
  );
}