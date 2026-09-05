"use client";

import {
  IndianRupee,
  Target,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";

import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { StatCard } from "@/components/dashboard/StatCard";
import { RevenueChart } from "@/components/dashboard/RevenueChart";
import { OpportunitySummary } from "@/components/dashboard/OpportuntySummary";
import { RecentOpportunities } from "@/components/dashboard/RecentOpportunities";

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        <section>
          <p className="text-sm font-medium text-[#146ef5]">
            Revenue Intelligence
          </p>

          <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 lg:text-4xl">
            Turn payment signals into revenue.
          </h1>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
            Your AI revenue engine identifies recoverable,
            preventable and expandable revenue opportunities.
          </p>
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard
            title="Revenue at Risk"
            value="₹18.7L"
            subtitle="Across detected signals"
            icon={IndianRupee}
            trend="+12.4% vs previous period"
          />

          <StatCard
            title="Expected Recovery"
            value="₹11.4L"
            subtitle="Probability-weighted"
            icon={TrendingUp}
            trend="+8.7% opportunity growth"
          />

          <StatCard
            title="Opportunities"
            value="247"
            subtitle="Detected by engine"
            icon={Target}
          />

          <StatCard
            title="High Priority"
            value="38"
            subtitle="Require immediate action"
            icon={ShieldCheck}
          />
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.7fr_1fr]">
          <RevenueChart />

          <OpportunitySummary />
        </section>

        <section>
          <RecentOpportunities />
        </section>
      </div>
    </DashboardLayout>
  );
}