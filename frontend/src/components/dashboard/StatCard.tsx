import { LucideIcon } from "lucide-react";
import { Card } from "../ui/Card";

interface StatCardProps {
  title: string;
  value: string;
  subtitle: string;
  icon: LucideIcon;
  trend?: string;
}

export function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
}: StatCardProps) {
  return (
    <Card className="p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            {title}
          </p>

          <p className="mt-2 text-3xl font-bold tracking-tight text-slate-950">
            {value}
          </p>

          <p className="mt-1 text-xs text-slate-400">
            {subtitle}
          </p>
        </div>

        <div className="rounded-xl bg-blue-50 p-3 text-[#146ef5]">
          <Icon size={20} />
        </div>
      </div>

      {trend && (
        <div className="mt-4 text-xs font-semibold text-emerald-600">
          {trend}
        </div>
      )}
    </Card>
  );
}