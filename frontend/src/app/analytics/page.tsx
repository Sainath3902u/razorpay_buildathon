"use client";

import {
  Activity,
  ArrowDownRight,
  ArrowUpRight,
  BarChart3,
} from "lucide-react";

import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { Card } from "@/components/ui/Card";
import { formatCurrency } from "@/lib/utils";

export default function AnalyticsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-[#146ef5]">
            <BarChart3 size={23} />
          </div>

          <h1 className="mt-4 text-3xl font-bold tracking-tight text-slate-950">
            Analytics
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Understand where revenue is leaking and where
            growth can be unlocked.
          </p>
        </section>

        <div className="grid gap-5 md:grid-cols-3">
          <Card className="p-6">
            <Activity
              size={20}
              className="text-[#146ef5]"
            />

            <p className="mt-5 text-sm text-slate-500">
              Recovery rate
            </p>

            <p className="mt-1 text-3xl font-bold">
              84.2%
            </p>

            <p className="mt-2 flex items-center gap-1 text-xs font-semibold text-emerald-600">
              <ArrowUpRight size={14} />
              6.8% this period
            </p>
          </Card>

          <Card className="p-6">
            <Activity
              size={20}
              className="text-violet-500"
            />

            <p className="mt-5 text-sm text-slate-500">
              Revenue leakage
            </p>

            <p className="mt-1 text-3xl font-bold">
              {formatCurrency(1870000)}
            </p>

            <p className="mt-2 flex items-center gap-1 text-xs font-semibold text-red-600">
              <ArrowDownRight size={14} />
              4.2% this period
            </p>
          </Card>

          <Card className="p-6">
            <Activity
              size={20}
              className="text-emerald-500"
            />

            <p className="mt-5 text-sm text-slate-500">
              Expansion potential
            </p>

            <p className="mt-1 text-3xl font-bold">
              {formatCurrency(5200000)}
            </p>

            <p className="mt-2 flex items-center gap-1 text-xs font-semibold text-emerald-600">
              <ArrowUpRight size={14} />
              14.3% this period
            </p>
          </Card>
        </div>

        <Card className="p-6">
          <h2 className="font-semibold text-slate-950">
            Revenue opportunity distribution
          </h2>

          <div className="mt-8 space-y-6">
            {[
              ["Payment recovery", 82],
              ["Churn prevention", 67],
              ["Checkout optimization", 54],
              ["Customer expansion", 43],
            ].map(([label, value]) => (
              <div key={label}>
                <div className="mb-2 flex justify-between text-sm">
                  <span className="text-slate-600">
                    {label}
                  </span>

                  <span className="font-semibold">
                    {value}%
                  </span>
                </div>

                <div className="h-3 rounded-full bg-slate-100">
                  <div
                    className="h-full rounded-full bg-[#146ef5]"
                    style={{
                      width: `${value}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </DashboardLayout>
  );
}