// // // "use client";

// // // import {
// // //   IndianRupee,
// // //   Target,
// // //   ShieldCheck,
// // //   TrendingUp,
// // // } from "lucide-react";

// // // import { useEffect, useState } from "react";

// // // import { useDataset } from "@/hooks/useDataset";
// // // import { useOpportunities } from "@/hooks/useOpportunities";

// // // import { DashboardLayout } from "@/components/layout/DashboardLayout";
// // // import { StatCard } from "@/components/dashboard/StatCard";
// // // import { RevenueChart } from "@/components/dashboard/RevenueChart";
// // // import { OpportunitySummary } from "@/components/dashboard/OpportuntySummary";
// // // import { RecentOpportunities } from "@/components/dashboard/RecentOpportunities";

// // // export default function DashboardPage() {
// // //   return (
// // //     <DashboardLayout>
// // //       <div className="space-y-8">
// // //         <section>
// // //           <p className="text-sm font-medium text-[#146ef5]">
// // //             Revenue Intelligence
// // //           </p>

// // //           <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 lg:text-4xl">
// // //             Turn payment signals into revenue.
// // //           </h1>

// // //           <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
// // //             Your AI revenue engine identifies recoverable,
// // //             preventable and expandable revenue opportunities.
// // //           </p>
// // //         </section>

// // //         <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
// // //           <StatCard
// // //             title="Revenue at Risk"
// // //             value="₹18.7L"
// // //             subtitle="Across detected signals"
// // //             icon={IndianRupee}
// // //             trend="+12.4% vs previous period"
// // //           />

// // //           <StatCard
// // //             title="Expected Recovery"
// // //             value="₹11.4L"
// // //             subtitle="Probability-weighted"
// // //             icon={TrendingUp}
// // //             trend="+8.7% opportunity growth"
// // //           />

// // //           <StatCard
// // //             title="Opportunities"
// // //             value="247"
// // //             subtitle="Detected by engine"
// // //             icon={Target}
// // //           />

// // //           <StatCard
// // //             title="High Priority"
// // //             value="38"
// // //             subtitle="Require immediate action"
// // //             icon={ShieldCheck}
// // //           />
// // //         </section>

// // //         <section className="grid gap-6 xl:grid-cols-[1.7fr_1fr]">
// // //           <RevenueChart />

// // //           <OpportunitySummary />
// // //         </section>

// // //         <section>
// // //           <RecentOpportunities />
// // //         </section>
// // //       </div>
// // //     </DashboardLayout>
// // //   );
// // // }




// // "use client";

// // import {
// //   IndianRupee,
// //   Target,
// //   ShieldCheck,
// //   TrendingUp,
// // } from "lucide-react";

// // import { useDataset } from "@/hooks/useDataset";
// // import { useOpportunities } from "@/hooks/useOpportunities";

// // import { DashboardLayout } from "@/components/layout/DashboardLayout";
// // import { StatCard } from "@/components/dashboard/StatCard";
// // import { RevenueChart } from "@/components/dashboard/RevenueChart";
// // import { OpportunitySummary } from "@/components/dashboard/OpportuntySummary";
// // import { RecentOpportunities } from "@/components/dashboard/RecentOpportunities";

// // export default function DashboardPage() {
// //   const dataset = useDataset();

// //   const {
// //     opportunities,
// //     summary,
// //     loading,
// //     error,
// //   } = useOpportunities(dataset?.datasetId);

// //   /*
// //    * -----------------------------------------
// //    * REAL DATA FROM BACKEND
// //    * -----------------------------------------
// //    */

// //   const revenueAtRisk =
// //     summary?.total_amount_at_risk ?? 0;

// //   const expectedRecovery =
// //     summary?.total_expected_value ?? 0;

// //   const totalOpportunities =
// //     summary?.total_opportunities ??
// //     opportunities.length;

// //   const highPriority =
// //     summary?.priority_counts?.HIGH ?? 0;

// //   /*
// //    * Format money values for Indian currency.
// //    *
// //    * Example:
// //    * 187000 -> ₹1.87L
// //    * 1250000 -> ₹12.50L
// //    * 50000 -> ₹50.0K
// //    */
// //   const formatCurrency = (amount: number) => {
// //     if (!Number.isFinite(amount)) {
// //       return "₹0";
// //     }

// //     if (amount >= 10000000) {
// //       return `₹${(amount / 10000000).toFixed(2)}Cr`;
// //     }

// //     if (amount >= 100000) {
// //       return `₹${(amount / 100000).toFixed(2)}L`;
// //     }

// //     if (amount >= 1000) {
// //       return `₹${(amount / 1000).toFixed(1)}K`;
// //     }

// //     return `₹${Math.round(amount).toLocaleString("en-IN")}`;
// //   };

// //   /*
// //    * -----------------------------------------
// //    * LOADING STATE
// //    * -----------------------------------------
// //    */

// //   if (loading) {
// //     return (
// //       <DashboardLayout>
// //         <div className="space-y-8">
// //           <section>
// //             <p className="text-sm font-medium text-[#146ef5]">
// //               Revenue Intelligence
// //             </p>

// //             <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 lg:text-4xl">
// //               Turn payment signals into revenue.
// //             </h1>

// //             <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
// //               Analyzing your dataset and detecting revenue
// //               opportunities...
// //             </p>
// //           </section>

// //           <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
// //             <StatCard
// //               title="Revenue at Risk"
// //               value="..."
// //               subtitle="Analyzing dataset"
// //               icon={IndianRupee}
// //             />

// //             <StatCard
// //               title="Expected Recovery"
// //               value="..."
// //               subtitle="Calculating"
// //               icon={TrendingUp}
// //             />

// //             <StatCard
// //               title="Opportunities"
// //               value="..."
// //               subtitle="Detecting opportunities"
// //               icon={Target}
// //             />

// //             <StatCard
// //               title="High Priority"
// //               value="..."
// //               subtitle="Calculating priority"
// //               icon={ShieldCheck}
// //             />
// //           </section>
// //         </div>
// //       </DashboardLayout>
// //     );
// //   }

// //   /*
// //    * -----------------------------------------
// //    * NO DATASET
// //    * -----------------------------------------
// //    */

// //   if (!dataset?.datasetId) {
// //     return (
// //       <DashboardLayout>
// //         <div className="space-y-8">
// //           <section>
// //             <p className="text-sm font-medium text-[#146ef5]">
// //               Revenue Intelligence
// //             </p>

// //             <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 lg:text-4xl">
// //               Turn payment signals into revenue.
// //             </h1>

// //             <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
// //               Upload a dataset to discover recoverable,
// //               preventable and expandable revenue opportunities.
// //             </p>
// //           </section>

// //           <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
// //             <Target className="mx-auto h-10 w-10 text-slate-400" />

// //             <h2 className="mt-4 text-lg font-semibold text-slate-900">
// //               No dataset uploaded
// //             </h2>

// //             <p className="mt-2 text-sm text-slate-500">
// //               Upload a payment or revenue dataset to populate
// //               the dashboard with real analysis.
// //             </p>
// //           </div>
// //         </div>
// //       </DashboardLayout>
// //     );
// //   }

// //   /*
// //    * -----------------------------------------
// //    * API ERROR
// //    * -----------------------------------------
// //    */

// //   if (error) {
// //     return (
// //       <DashboardLayout>
// //         <div className="space-y-8">
// //           <section>
// //             <p className="text-sm font-medium text-[#146ef5]">
// //               Revenue Intelligence
// //             </p>

// //             <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 lg:text-4xl">
// //               Turn payment signals into revenue.
// //             </h1>

// //             <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
// //               Your AI revenue engine identifies recoverable,
// //               preventable and expandable revenue opportunities.
// //             </p>
// //           </section>

// //           <div className="rounded-2xl border border-red-200 bg-red-50 p-6">
// //             <h2 className="font-semibold text-red-900">
// //               Unable to load dashboard data
// //             </h2>

// //             <p className="mt-2 text-sm text-red-700">
// //               {error}
// //             </p>

// //             <p className="mt-3 text-xs text-red-600">
// //               Dataset ID: {dataset.datasetId}
// //             </p>
// //           </div>
// //         </div>
// //       </DashboardLayout>
// //     );
// //   }

// //   /*
// //    * -----------------------------------------
// //    * MAIN DASHBOARD
// //    * -----------------------------------------
// //    */

// //   return (
// //     <DashboardLayout>
// //       <div className="space-y-8">
// //         {/* Header */}
// //         <section>
// //           <p className="text-sm font-medium text-[#146ef5]">
// //             Revenue Intelligence
// //           </p>

// //           <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 lg:text-4xl">
// //             Turn payment signals into revenue.
// //           </h1>

// //           <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
// //             Your AI revenue engine identifies recoverable,
// //             preventable and expandable revenue opportunities.
// //           </p>

// //           {dataset.filename && (
// //             <p className="mt-2 text-xs text-slate-400">
// //               Analyzing:{" "}
// //               <span className="font-medium text-slate-500">
// //                 {dataset.filename}
// //               </span>
// //             </p>
// //           )}
// //         </section>

// //         {/* Real KPI Cards */}
// //         <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
// //           <StatCard
// //             title="Revenue at Risk"
// //             value={formatCurrency(revenueAtRisk)}
// //             subtitle="Across detected signals"
// //             icon={IndianRupee}
// //           />

// //           <StatCard
// //             title="Expected Recovery"
// //             value={formatCurrency(expectedRecovery)}
// //             subtitle="Probability-weighted"
// //             icon={TrendingUp}
// //           />

// //           <StatCard
// //             title="Opportunities"
// //             value={totalOpportunities.toLocaleString("en-IN")}
// //             subtitle="Detected by engine"
// //             icon={Target}
// //           />

// //           <StatCard
// //             title="High Priority"
// //             value={highPriority.toLocaleString("en-IN")}
// //             subtitle="Require immediate action"
// //             icon={ShieldCheck}
// //           />
// //         </section>

// //         {/* Charts / Summary */}
// //         <section className="grid gap-6 xl:grid-cols-[1.7fr_1fr]">
// //           <RevenueChart
// //             opportunities={opportunities}
// //           />

// //           <OpportunitySummary
// //             summary={summary}
// //             opportunities={opportunities}
// //           />
// //         </section>

// //         {/* Recent Opportunities */}
// //         <section>
// //           <RecentOpportunities
// //             opportunities={opportunities}
// //           />
// //         </section>
// //       </div>
// //     </DashboardLayout>
// //   );
// // }


// "use client";

// import {
//   IndianRupee,
//   Target,
//   ShieldCheck,
//   TrendingUp,
// } from "lucide-react";

// import { useDataset } from "@/hooks/useDataset";
// import { useOpportunities } from "@/hooks/useOpportunities";

// import { DashboardLayout } from "@/components/layout/DashboardLayout";
// import { StatCard } from "@/components/dashboard/StatCard";
// import { RevenueChart } from "@/components/dashboard/RevenueChart";
// import { OpportunitySummary } from "@/components/dashboard/OpportuntySummary";
// import { RecentOpportunities } from "@/components/dashboard/RecentOpportunities";

// export default function DashboardPage() {
//   /*
//    * useDataset() returns:
//    *
//    * {
//    *   dataset,
//    *   saveDataset,
//    *   clearDataset
//    * }
//    */
//   const { dataset } = useDataset();

//   /*
//    * dataset can be null, so safely access datasetId.
//    */
//   const datasetId = dataset?.datasetId ?? null;

//   /*
//    * Fetch real analysis from FastAPI.
//    */
//   const {
//     opportunities,
//     summary,
//     loading,
//     error,
//   } = useOpportunities(datasetId);

//   /*
//    * -----------------------------------------
//    * REAL BACKEND VALUES
//    * -----------------------------------------
//    */

//   const revenueAtRisk =
//     summary?.total_amount_at_risk ?? 0;

//   const expectedRecovery =
//     summary?.total_expected_value ?? 0;

//   const totalOpportunities =
//     summary?.total_opportunities ??
//     opportunities.length;

//   const highPriority =
//     summary?.priority_counts?.HIGH ?? 0;

//   /*
//    * -----------------------------------------
//    * CURRENCY FORMATTER
//    * -----------------------------------------
//    */

//   const formatCurrency = (amount: number) => {
//     if (!Number.isFinite(amount)) {
//       return "₹0";
//     }

//     if (amount >= 10000000) {
//       return `₹${(amount / 10000000).toFixed(2)}Cr`;
//     }

//     if (amount >= 100000) {
//       return `₹${(amount / 100000).toFixed(2)}L`;
//     }

//     if (amount >= 1000) {
//       return `₹${(amount / 1000).toFixed(1)}K`;
//     }

//     return `₹${Math.round(amount).toLocaleString("en-IN")}`;
//   };

//   /*
//    * -----------------------------------------
//    * NO DATASET
//    * -----------------------------------------
//    */

//   if (!datasetId) {
//     return (
//       <DashboardLayout>
//         <div className="space-y-8">
//           <section>
//             <p className="text-sm font-medium text-[#146ef5]">
//               Revenue Intelligence
//             </p>

//             <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 lg:text-4xl">
//               Turn payment signals into revenue.
//             </h1>

//             <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
//               Upload a dataset to discover recoverable,
//               preventable and expandable revenue opportunities.
//             </p>
//           </section>

//           <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
//             <Target className="mx-auto h-10 w-10 text-slate-400" />

//             <h2 className="mt-4 text-lg font-semibold text-slate-900">
//               No dataset uploaded
//             </h2>

//             <p className="mt-2 text-sm text-slate-500">
//               Upload a payment or revenue dataset to populate
//               the dashboard with real analysis.
//             </p>
//           </div>
//         </div>
//       </DashboardLayout>
//     );
//   }

//   /*
//    * -----------------------------------------
//    * API ERROR
//    * -----------------------------------------
//    */

//   if (error) {
//     return (
//       <DashboardLayout>
//         <div className="space-y-8">
//           <section>
//             <p className="text-sm font-medium text-[#146ef5]">
//               Revenue Intelligence
//             </p>

//             <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 lg:text-4xl">
//               Turn payment signals into revenue.
//             </h1>

//             <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
//               Your AI revenue engine identifies recoverable,
//               preventable and expandable revenue opportunities.
//             </p>
//           </section>

//           <div className="rounded-2xl border border-red-200 bg-red-50 p-6">
//             <h2 className="font-semibold text-red-900">
//               Unable to load dashboard data
//             </h2>

//             <p className="mt-2 text-sm text-red-700">
//               {error}
//             </p>

//             <p className="mt-3 text-xs text-red-600">
//               Dataset ID: {datasetId}
//             </p>
//           </div>
//         </div>
//       </DashboardLayout>
//     );
//   }

//   /*
//    * -----------------------------------------
//    * DASHBOARD
//    * -----------------------------------------
//    */

//   return (
//     <DashboardLayout>
//       <div className="space-y-8">

//         {/* Header */}
//         <section>
//           <p className="text-sm font-medium text-[#146ef5]">
//             Revenue Intelligence
//           </p>

//           <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 lg:text-4xl">
//             Turn payment signals into revenue.
//           </h1>

//           <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
//             Your AI revenue engine identifies recoverable,
//             preventable and expandable revenue opportunities.
//           </p>

//           {dataset.filename && (
//             <p className="mt-2 text-xs text-slate-400">
//               Analyzing:{" "}
//               <span className="font-medium text-slate-500">
//                 {dataset.filename}
//               </span>
//             </p>
//           )}
//         </section>

//         {/* KPI Cards */}
//         <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

//           <StatCard
//             title="Revenue at Risk"
//             value={
//               loading
//                 ? "..."
//                 : formatCurrency(revenueAtRisk)
//             }
//             subtitle="Across detected signals"
//             icon={IndianRupee}
//           />

//           <StatCard
//             title="Expected Recovery"
//             value={
//               loading
//                 ? "..."
//                 : formatCurrency(expectedRecovery)
//             }
//             subtitle="Probability-weighted"
//             icon={TrendingUp}
//           />

//           <StatCard
//             title="Opportunities"
//             value={
//               loading
//                 ? "..."
//                 : totalOpportunities.toLocaleString("en-IN")
//             }
//             subtitle="Detected by engine"
//             icon={Target}
//           />

//           <StatCard
//             title="High Priority"
//             value={
//               loading
//                 ? "..."
//                 : highPriority.toLocaleString("en-IN")
//             }
//             subtitle="Require immediate action"
//             icon={ShieldCheck}
//           />

//         </section>

//         {/* Existing dashboard components */}
//         <section className="grid gap-6 xl:grid-cols-[1.7fr_1fr]">

//           <RevenueChart />

//           <OpportunitySummary />

//         </section>

//         <section>
//           <RecentOpportunities />
//         </section>

//       </div>
//     </DashboardLayout>
//   );
// }



"use client";

import {
  IndianRupee,
  Target,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";

import { useDataset } from "@/hooks/useDataset";
import { useOpportunities } from "@/hooks/useOpportunities";

import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { StatCard } from "@/components/dashboard/StatCard";
import { RevenueChart } from "@/components/dashboard/RevenueChart";
import { OpportunitySummary } from "@/components/dashboard/OpportunitySummary";
import { RecentOpportunities } from "@/components/dashboard/RecentOpportunities";

export default function DashboardPage() {
  const { dataset } = useDataset();

  /*
   * dataset can be null.
   * Safely extract the values we need.
   */
  const datasetId = dataset?.datasetId ?? null;
  const filename = dataset?.filename ?? null;

  /*
   * Fetch real opportunities from FastAPI.
   */
  const {
    opportunities,
    summary,
    loading,
    error,
  } = useOpportunities(datasetId);

  /*
   * -----------------------------------------
   * REAL BACKEND DATA
   * -----------------------------------------
   */

  const revenueAtRisk =
    summary?.total_amount_at_risk ?? 0;

  const expectedRecovery =
    summary?.total_expected_value ?? 0;

  const totalOpportunities =
    summary?.total_opportunities ??
    opportunities.length;

  const highPriority =
    summary?.priority_counts?.HIGH ?? 0;

  /*
   * -----------------------------------------
   * CURRENCY FORMATTER
   * -----------------------------------------
   */

  const formatCurrency = (amount: number) => {
    if (!Number.isFinite(amount)) {
      return "₹0";
    }

    if (amount >= 10000000) {
      return `₹${(amount / 10000000).toFixed(2)}Cr`;
    }

    if (amount >= 100000) {
      return `₹${(amount / 100000).toFixed(2)}L`;
    }

    if (amount >= 1000) {
      return `₹${(amount / 1000).toFixed(1)}K`;
    }

    return `₹${Math.round(amount).toLocaleString("en-IN")}`;
  };

  /*
   * -----------------------------------------
   * NO DATASET
   * -----------------------------------------
   */

  if (!datasetId) {
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
              Upload a dataset to discover recoverable,
              preventable and expandable revenue opportunities.
            </p>
          </section>

          <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">

            <Target className="mx-auto h-10 w-10 text-slate-400" />

            <h2 className="mt-4 text-lg font-semibold text-slate-900">
              No dataset uploaded
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Upload a payment or revenue dataset to populate
              the dashboard with real analysis.
            </p>

          </div>

        </div>
      </DashboardLayout>
    );
  }

  /*
   * -----------------------------------------
   * API ERROR
   * -----------------------------------------
   */

  if (error) {
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

          <div className="rounded-2xl border border-red-200 bg-red-50 p-6">

            <h2 className="font-semibold text-red-900">
              Unable to load dashboard data
            </h2>

            <p className="mt-2 text-sm text-red-700">
              {error}
            </p>

            <p className="mt-3 text-xs text-red-600">
              Dataset ID: {datasetId}
            </p>

          </div>

        </div>
      </DashboardLayout>
    );
  }

  /*
   * -----------------------------------------
   * DASHBOARD
   * -----------------------------------------
   */

  return (
    <DashboardLayout>
      <div className="space-y-8">

        {/* Header */}
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

          {filename && (
            <p className="mt-2 text-xs text-slate-400">
              Analyzing:{" "}
              <span className="font-medium text-slate-500">
                {filename}
              </span>
            </p>
          )}

        </section>

        {/* Real KPI Cards */}
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

          <StatCard
            title="Revenue at Risk"
            value={
              loading
                ? "..."
                : formatCurrency(revenueAtRisk)
            }
            subtitle="Across detected signals"
            icon={IndianRupee}
          />

          <StatCard
            title="Expected Recovery"
            value={
              loading
                ? "..."
                : formatCurrency(expectedRecovery)
            }
            subtitle="Probability-weighted"
            icon={TrendingUp}
          />

          <StatCard
            title="Opportunities"
            value={
              loading
                ? "..."
                : totalOpportunities.toLocaleString("en-IN")
            }
            subtitle="Detected by engine"
            icon={Target}
          />

          <StatCard
            title="High Priority"
            value={
              loading
                ? "..."
                : highPriority.toLocaleString("en-IN")
            }
            subtitle="Require immediate action"
            icon={ShieldCheck}
          />

        </section>

            <section className="grid gap-6 xl:grid-cols-[1.7fr_1fr]">
      <RevenueChart opportunities={opportunities} />

      <OpportunitySummary
        summary={summary}
        opportunities={opportunities}
        />
      </section>

      <section>
        <RecentOpportunities
          opportunities={opportunities}
        />
      </section>

      </div>
    </DashboardLayout>
  );
}