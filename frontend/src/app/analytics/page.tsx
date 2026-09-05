// // "use client";

// // import {
// //   Activity,
// //   ArrowDownRight,
// //   ArrowUpRight,
// //   BarChart3,
// // } from "lucide-react";

// // import { DashboardLayout } from "@/components/layout/DashboardLayout";
// // import { Card } from "@/components/ui/Card";
// // import { formatCurrency } from "@/lib/utils";

// // export default function AnalyticsPage() {
// //   return (
// //     <DashboardLayout>
// //       <div className="space-y-8">
// //         <section>
// //           <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-[#146ef5]">
// //             <BarChart3 size={23} />
// //           </div>

// //           <h1 className="mt-4 text-3xl font-bold tracking-tight text-slate-950">
// //             Analytics
// //           </h1>

// //           <p className="mt-2 text-sm text-slate-500">
// //             Understand where revenue is leaking and where
// //             growth can be unlocked.
// //           </p>
// //         </section>

// //         <div className="grid gap-5 md:grid-cols-3">
// //           <Card className="p-6">
// //             <Activity
// //               size={20}
// //               className="text-[#146ef5]"
// //             />

// //             <p className="mt-5 text-sm text-slate-500">
// //               Recovery rate
// //             </p>

// //             <p className="mt-1 text-3xl font-bold">
// //               84.2%
// //             </p>

// //             <p className="mt-2 flex items-center gap-1 text-xs font-semibold text-emerald-600">
// //               <ArrowUpRight size={14} />
// //               6.8% this period
// //             </p>
// //           </Card>

// //           <Card className="p-6">
// //             <Activity
// //               size={20}
// //               className="text-violet-500"
// //             />

// //             <p className="mt-5 text-sm text-slate-500">
// //               Revenue leakage
// //             </p>

// //             <p className="mt-1 text-3xl font-bold">
// //               {formatCurrency(1870000)}
// //             </p>

// //             <p className="mt-2 flex items-center gap-1 text-xs font-semibold text-red-600">
// //               <ArrowDownRight size={14} />
// //               4.2% this period
// //             </p>
// //           </Card>

// //           <Card className="p-6">
// //             <Activity
// //               size={20}
// //               className="text-emerald-500"
// //             />

// //             <p className="mt-5 text-sm text-slate-500">
// //               Expansion potential
// //             </p>

// //             <p className="mt-1 text-3xl font-bold">
// //               {formatCurrency(5200000)}
// //             </p>

// //             <p className="mt-2 flex items-center gap-1 text-xs font-semibold text-emerald-600">
// //               <ArrowUpRight size={14} />
// //               14.3% this period
// //             </p>
// //           </Card>
// //         </div>

// //         <Card className="p-6">
// //           <h2 className="font-semibold text-slate-950">
// //             Revenue opportunity distribution
// //           </h2>

// //           <div className="mt-8 space-y-6">
// //             {[
// //               ["Payment recovery", 82],
// //               ["Churn prevention", 67],
// //               ["Checkout optimization", 54],
// //               ["Customer expansion", 43],
// //             ].map(([label, value]) => (
// //               <div key={label}>
// //                 <div className="mb-2 flex justify-between text-sm">
// //                   <span className="text-slate-600">
// //                     {label}
// //                   </span>

// //                   <span className="font-semibold">
// //                     {value}%
// //                   </span>
// //                 </div>

// //                 <div className="h-3 rounded-full bg-slate-100">
// //                   <div
// //                     className="h-full rounded-full bg-[#146ef5]"
// //                     style={{
// //                       width: `${value}%`,
// //                     }}
// //                   />
// //                 </div>
// //               </div>
// //             ))}
// //           </div>
// //         </Card>
// //       </div>
// //     </DashboardLayout>
// //   );
// // }






// "use client";

// import {
//   TrendingUp,
//   IndianRupee,
//   Target,
//   Activity,
// } from "lucide-react";

// import { useDataset } from "@/hooks/useDataset";
// import { useOpportunities } from "@/hooks/useOpportunities";

// import { DashboardLayout } from "@/components/layout/DashboardLayout";
// import { Card } from "@/components/ui/Card";

// export default function AnalyticsPage() {
//   const { dataset } = useDataset();

//   /*
//    * dataset can be null.
//    */
//   const datasetId = dataset?.datasetId ?? null;

//   /*
//    * Get REAL data from FastAPI.
//    */
//   const {
//     opportunities,
//     summary,
//     loading,
//     error,
//   } = useOpportunities(datasetId);

//   /*
//    * -----------------------------------------
//    * REAL VALUES
//    * -----------------------------------------
//    */

//   const revenueAtRisk =
//     summary?.total_amount_at_risk ?? 0;

//   const expectedRecovery =
//     summary?.total_expected_value ?? 0;

//   const totalOpportunities =
//     summary?.total_opportunities ??
//     opportunities.length;

//   /*
//    * Category counts from backend.
//    */
//   const recoverCount =
//     summary?.category_counts?.RECOVER ??
//     opportunities.filter(
//       (item) => item.category === "RECOVER"
//     ).length;

//   const preventCount =
//     summary?.category_counts?.PREVENT ??
//     opportunities.filter(
//       (item) => item.category === "PREVENT"
//     ).length;

//   const growCount =
//     summary?.category_counts?.GROW ??
//     opportunities.filter(
//       (item) => item.category === "GROW"
//     ).length;

//   /*
//    * -----------------------------------------
//    * ANALYTICS CALCULATIONS
//    * -----------------------------------------
//    */

//   /*
//    * Recovery rate =
//    * expected recovery / revenue at risk
//    */
//   const recoveryRate =
//     revenueAtRisk > 0
//       ? Math.min(
//           100,
//           (expectedRecovery /
//             revenueAtRisk) *
//             100
//         )
//       : 0;

//   /*
//    * Expansion potential =
//    * expected value of GROW opportunities.
//    */
//   const expansionPotential =
//     opportunities
//       .filter(
//         (item) => item.category === "GROW"
//       )
//       .reduce(
//         (sum, item) =>
//           sum + (item.expected_value || 0),
//         0
//       );

//   /*
//    * Category distribution.
//    */
//   const totalCategories =
//     recoverCount +
//     preventCount +
//     growCount;

//   const recoverPercentage =
//     totalCategories > 0
//       ? (recoverCount /
//           totalCategories) *
//         100
//       : 0;

//   const preventPercentage =
//     totalCategories > 0
//       ? (preventCount /
//           totalCategories) *
//         100
//       : 0;

//   const growPercentage =
//     totalCategories > 0
//       ? (growCount /
//           totalCategories) *
//         100
//       : 0;

//   /*
//    * -----------------------------------------
//    * FORMATTERS
//    * -----------------------------------------
//    */

//   const formatCurrency = (
//     amount: number
//   ) => {
//     if (!Number.isFinite(amount)) {
//       return "₹0";
//     }

//     if (amount >= 10000000) {
//       return `₹${(
//         amount / 10000000
//       ).toFixed(2)}Cr`;
//     }

//     if (amount >= 100000) {
//       return `₹${(
//         amount / 100000
//       ).toFixed(2)}L`;
//     }

//     if (amount >= 1000) {
//       return `₹${(
//         amount / 1000
//       ).toFixed(1)}K`;
//     }

//     return `₹${Math.round(
//       amount
//     ).toLocaleString("en-IN")}`;
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
//               Analytics
//             </h1>

//             <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
//               Understand where revenue is leaking
//               and where growth can be unlocked.
//             </p>
//           </section>

//           <Card className="p-10 text-center">

//             <Target className="mx-auto h-10 w-10 text-slate-300" />

//             <h2 className="mt-4 text-lg font-semibold text-slate-900">
//               No dataset uploaded
//             </h2>

//             <p className="mt-2 text-sm text-slate-500">
//               Upload a dataset to generate real
//               revenue analytics.
//             </p>

//           </Card>

//         </div>
//       </DashboardLayout>
//     );
//   }

//   /*
//    * -----------------------------------------
//    * ERROR
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
//               Analytics
//             </h1>

//             <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
//               Understand where revenue is leaking
//               and where growth can be unlocked.
//             </p>
//           </section>

//           <Card className="border-red-200 bg-red-50 p-6">

//             <h2 className="font-semibold text-red-900">
//               Unable to load analytics
//             </h2>

//             <p className="mt-2 text-sm text-red-700">
//               {error}
//             </p>

//             <p className="mt-3 text-xs text-red-600">
//               Dataset ID: {datasetId}
//             </p>

//           </Card>

//         </div>
//       </DashboardLayout>
//     );
//   }

//   /*
//    * -----------------------------------------
//    * MAIN ANALYTICS PAGE
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
//             Analytics
//           </h1>

//           <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
//             Understand where revenue is leaking
//             and where growth can be unlocked.
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

//         {/* Loading */}
//         {loading && (
//           <div className="rounded-xl border border-slate-200 bg-white p-4 text-sm text-slate-500">
//             Analyzing uploaded dataset...
//           </div>
//         )}

//         {/* KPI CARDS */}
//         <section className="grid gap-6 lg:grid-cols-3">

//           {/* Recovery Rate */}
//           <Card className="p-7">

//             <div className="flex h-10 w-10 items-center justify-center text-[#146ef5]">
//               <Activity className="h-7 w-7" />
//             </div>

//             <p className="mt-6 text-sm text-slate-500">
//               Recovery rate
//             </p>

//             <p className="mt-1 text-4xl font-bold text-slate-950">
//               {loading
//                 ? "..."
//                 : `${recoveryRate.toFixed(1)}%`}
//             </p>

//             <p className="mt-4 text-xs text-slate-400">
//               Expected recovery relative to
//               identified revenue at risk
//             </p>

//           </Card>

//           {/* Revenue Leakage */}
//           <Card className="p-7">

//             <div className="flex h-10 w-10 items-center justify-center text-[#146ef5]">
//               <IndianRupee className="h-7 w-7" />
//             </div>

//             <p className="mt-6 text-sm text-slate-500">
//               Revenue leakage
//             </p>

//             <p className="mt-1 text-4xl font-bold text-slate-950">
//               {loading
//                 ? "..."
//                 : formatCurrency(
//                     revenueAtRisk
//                   )}
//             </p>

//             <p className="mt-4 text-xs text-slate-400">
//               Total amount at risk detected
//               in the uploaded dataset
//             </p>

//           </Card>

//           {/* Expansion Potential */}
//           <Card className="p-7">

//             <div className="flex h-10 w-10 items-center justify-center text-emerald-500">
//               <TrendingUp className="h-7 w-7" />
//             </div>

//             <p className="mt-6 text-sm text-slate-500">
//               Expansion potential
//             </p>

//             <p className="mt-1 text-4xl font-bold text-slate-950">
//               {loading
//                 ? "..."
//                 : formatCurrency(
//                     expansionPotential
//                   )}
//             </p>

//             <p className="mt-4 text-xs text-slate-400">
//               Expected value from detected
//               growth opportunities
//             </p>

//           </Card>

//         </section>

//         {/* CATEGORY DISTRIBUTION */}
//         <Card className="p-7">

//           <div className="flex items-start justify-between">

//             <div>
//               <h2 className="text-lg font-semibold text-slate-950">
//                 Revenue opportunity distribution
//               </h2>

//               <p className="mt-1 text-sm text-slate-400">
//                 Distribution of opportunities detected
//                 in your dataset
//               </p>
//             </div>

//             <div className="text-right">
//               <p className="text-2xl font-bold text-slate-950">
//                 {totalOpportunities}
//               </p>

//               <p className="text-xs text-slate-400">
//                 total opportunities
//               </p>
//             </div>

//           </div>

//           {totalCategories === 0 ? (
//             <div className="flex min-h-[220px] items-center justify-center text-center">

//               <div>
//                 <Target className="mx-auto h-8 w-8 text-slate-300" />

//                 <p className="mt-3 text-sm font-medium text-slate-600">
//                   No opportunities detected
//                 </p>

//                 <p className="mt-1 text-xs text-slate-400">
//                   Try uploading a dataset with supported
//                   revenue/payment columns.
//                 </p>
//               </div>

//             </div>
//           ) : (
//             <div className="mt-8 space-y-7">

//               {/* Recover */}
//               <div>

//                 <div className="mb-2 flex justify-between">

//                   <span className="text-sm font-medium text-slate-700">
//                     Recover
//                   </span>

//                   <span className="text-sm font-semibold text-slate-950">
//                     {recoverCount}{" "}
//                     <span className="font-normal text-slate-400">
//                       ({recoverPercentage.toFixed(1)}%)
//                     </span>
//                   </span>

//                 </div>

//                 <div className="h-3 overflow-hidden rounded-full bg-slate-100">

//                   <div
//                     className="h-full rounded-full bg-blue-500 transition-all duration-500"
//                     style={{
//                       width: `${recoverPercentage}%`,
//                     }}
//                   />

//                 </div>

//               </div>

//               {/* Prevent */}
//               <div>

//                 <div className="mb-2 flex justify-between">

//                   <span className="text-sm font-medium text-slate-700">
//                     Prevent
//                   </span>

//                   <span className="text-sm font-semibold text-slate-950">
//                     {preventCount}{" "}
//                     <span className="font-normal text-slate-400">
//                       ({preventPercentage.toFixed(1)}%)
//                     </span>
//                   </span>

//                 </div>

//                 <div className="h-3 overflow-hidden rounded-full bg-slate-100">

//                   <div
//                     className="h-full rounded-full bg-violet-500 transition-all duration-500"
//                     style={{
//                       width: `${preventPercentage}%`,
//                     }}
//                   />

//                 </div>

//               </div>

//               {/* Grow */}
//               <div>

//                 <div className="mb-2 flex justify-between">

//                   <span className="text-sm font-medium text-slate-700">
//                     Grow
//                   </span>

//                   <span className="text-sm font-semibold text-slate-950">
//                     {growCount}{" "}
//                     <span className="font-normal text-slate-400">
//                       ({growPercentage.toFixed(1)}%)
//                     </span>
//                   </span>

//                 </div>

//                 <div className="h-3 overflow-hidden rounded-full bg-slate-100">

//                   <div
//                     className="h-full rounded-full bg-emerald-500 transition-all duration-500"
//                     style={{
//                       width: `${growPercentage}%`,
//                     }}
//                   />

//                 </div>

//               </div>

//             </div>
//           )}

//         </Card>

//         {/* DATASET SUMMARY */}
//         <Card className="p-7">

//           <div className="flex items-center gap-3">

//             <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50 text-[#146ef5]">
//               <Target className="h-5 w-5" />
//             </div>

//             <div>
//               <h2 className="font-semibold text-slate-950">
//                 Dataset analysis
//               </h2>

//               <p className="text-xs text-slate-400">
//                 Results generated from your uploaded data
//               </p>
//             </div>

//           </div>

//           <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

//             <div className="rounded-xl bg-slate-50 p-4">

//               <p className="text-xs text-slate-400">
//                 Dataset
//               </p>

//               <p className="mt-1 truncate text-sm font-semibold text-slate-800">
//                 {dataset.filename ?? "Uploaded dataset"}
//               </p>

//             </div>

//             <div className="rounded-xl bg-slate-50 p-4">

//               <p className="text-xs text-slate-400">
//                 Rows
//               </p>

//               <p className="mt-1 text-lg font-semibold text-slate-800">
//                 {dataset.rows.toLocaleString(
//                   "en-IN"
//                 )}
//               </p>

//             </div>

//             <div className="rounded-xl bg-slate-50 p-4">

//               <p className="text-xs text-slate-400">
//                 Columns
//               </p>

//               <p className="mt-1 text-lg font-semibold text-slate-800">
//                 {dataset.columns.toLocaleString(
//                   "en-IN"
//                 )}
//               </p>

//             </div>

//             <div className="rounded-xl bg-slate-50 p-4">

//               <p className="text-xs text-slate-400">
//                 Opportunities
//               </p>

//               <p className="mt-1 text-lg font-semibold text-slate-800">
//                 {totalOpportunities.toLocaleString(
//                   "en-IN"
//                 )}
//               </p>

//             </div>

//           </div>

//         </Card>

//       </div>
//     </DashboardLayout>
//   );
// }




"use client";

import {
  Activity,
  IndianRupee,
  Target,
  TrendingUp,
} from "lucide-react";

import { useDataset } from "@/hooks/useDataset";
import { useOpportunities } from "@/hooks/useOpportunities";

import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { Card } from "@/components/ui/Card";

export default function AnalyticsPage() {
  const { dataset } = useDataset();

  /*
   * Safely extract dataset information.
   * dataset can be null.
   */
  const datasetId = dataset?.datasetId ?? null;

  const datasetFilename =
    dataset?.filename ?? "Uploaded dataset";

  const datasetRows =
    dataset?.rows ?? 0;

  const datasetColumns =
    dataset?.columns ?? 0;

  /*
   * Fetch real analysis from FastAPI.
   */
  const {
    opportunities,
    summary,
    loading,
    error,
  } = useOpportunities(datasetId);

  /*
   * -----------------------------------------
   * REAL BACKEND VALUES
   * -----------------------------------------
   */

  const revenueAtRisk =
    summary?.total_amount_at_risk ?? 0;

  const expectedRecovery =
    summary?.total_expected_value ?? 0;

  const totalOpportunities =
    summary?.total_opportunities ??
    opportunities.length;

  /*
   * Category counts
   */
  const recoverCount =
    summary?.category_counts?.RECOVER ??
    opportunities.filter(
      (item) => item.category === "RECOVER"
    ).length;

  const preventCount =
    summary?.category_counts?.PREVENT ??
    opportunities.filter(
      (item) => item.category === "PREVENT"
    ).length;

  const growCount =
    summary?.category_counts?.GROW ??
    opportunities.filter(
      (item) => item.category === "GROW"
    ).length;

  /*
   * -----------------------------------------
   * CALCULATIONS
   * -----------------------------------------
   */

  const recoveryRate =
    revenueAtRisk > 0
      ? Math.min(
          100,
          (expectedRecovery / revenueAtRisk) * 100
        )
      : 0;

  /*
   * Expansion potential is the total expected
   * value of GROW opportunities.
   */
  const expansionPotential =
    opportunities
      .filter(
        (item) => item.category === "GROW"
      )
      .reduce(
        (sum, item) =>
          sum + (item.expected_value || 0),
        0
      );

  const totalCategories =
    recoverCount +
    preventCount +
    growCount;

  const recoverPercentage =
    totalCategories > 0
      ? (recoverCount / totalCategories) * 100
      : 0;

  const preventPercentage =
    totalCategories > 0
      ? (preventCount / totalCategories) * 100
      : 0;

  const growPercentage =
    totalCategories > 0
      ? (growCount / totalCategories) * 100
      : 0;

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
      return `₹${(
        amount / 10000000
      ).toFixed(2)}Cr`;
    }

    if (amount >= 100000) {
      return `₹${(
        amount / 100000
      ).toFixed(2)}L`;
    }

    if (amount >= 1000) {
      return `₹${(
        amount / 1000
      ).toFixed(1)}K`;
    }

    return `₹${Math.round(
      amount
    ).toLocaleString("en-IN")}`;
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
              Analytics
            </h1>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
              Understand where revenue is leaking
              and where growth can be unlocked.
            </p>
          </section>

          <Card className="p-10 text-center">

            <Target className="mx-auto h-10 w-10 text-slate-300" />

            <h2 className="mt-4 text-lg font-semibold text-slate-900">
              No dataset uploaded
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Upload a dataset to generate real
              revenue analytics.
            </p>

          </Card>

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
              Analytics
            </h1>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
              Understand where revenue is leaking
              and where growth can be unlocked.
            </p>
          </section>

          <Card className="border-red-200 bg-red-50 p-6">

            <h2 className="font-semibold text-red-900">
              Unable to load analytics
            </h2>

            <p className="mt-2 text-sm text-red-700">
              {error}
            </p>

            <p className="mt-3 text-xs text-red-600">
              Dataset ID: {datasetId}
            </p>

          </Card>

        </div>
      </DashboardLayout>
    );
  }

  /*
   * -----------------------------------------
   * MAIN ANALYTICS
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
            Analytics
          </h1>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
            Understand where revenue is leaking
            and where growth can be unlocked.
          </p>

          <p className="mt-2 text-xs text-slate-400">
            Analyzing:{" "}
            <span className="font-medium text-slate-500">
              {datasetFilename}
            </span>
          </p>

        </section>

        {/* Loading indicator */}
        {loading && (
          <div className="rounded-xl border border-blue-100 bg-blue-50 px-5 py-3 text-sm text-blue-700">
            Analyzing uploaded dataset...
          </div>
        )}

        {/* KPI CARDS */}
        <section className="grid gap-6 lg:grid-cols-3">

          {/* Recovery Rate */}
          <Card className="p-7">

            <div className="flex h-10 w-10 items-center justify-center text-[#146ef5]">
              <Activity className="h-7 w-7" />
            </div>

            <p className="mt-6 text-sm text-slate-500">
              Recovery rate
            </p>

            <p className="mt-1 text-4xl font-bold text-slate-950">
              {loading
                ? "..."
                : `${recoveryRate.toFixed(1)}%`}
            </p>

            <p className="mt-4 text-xs text-slate-400">
              Expected recovery relative to
              identified revenue at risk
            </p>

          </Card>

          {/* Revenue Leakage */}
          <Card className="p-7">

            <div className="flex h-10 w-10 items-center justify-center text-[#146ef5]">
              <IndianRupee className="h-7 w-7" />
            </div>

            <p className="mt-6 text-sm text-slate-500">
              Revenue leakage
            </p>

            <p className="mt-1 text-4xl font-bold text-slate-950">
              {loading
                ? "..."
                : formatCurrency(
                    revenueAtRisk
                  )}
            </p>

            <p className="mt-4 text-xs text-slate-400">
              Total amount at risk detected
              in the uploaded dataset
            </p>

          </Card>

          {/* Expansion Potential */}
          <Card className="p-7">

            <div className="flex h-10 w-10 items-center justify-center text-emerald-500">
              <TrendingUp className="h-7 w-7" />
            </div>

            <p className="mt-6 text-sm text-slate-500">
              Expansion potential
            </p>

            <p className="mt-1 text-4xl font-bold text-slate-950">
              {loading
                ? "..."
                : formatCurrency(
                    expansionPotential
                  )}
            </p>

            <p className="mt-4 text-xs text-slate-400">
              Expected value from detected
              growth opportunities
            </p>

          </Card>

        </section>

        {/* OPPORTUNITY DISTRIBUTION */}
        <Card className="p-7">

          <div className="flex items-start justify-between">

            <div>
              <h2 className="text-lg font-semibold text-slate-950">
                Revenue opportunity distribution
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Distribution of opportunities detected
                in your dataset
              </p>
            </div>

            <div className="text-right">

              <p className="text-2xl font-bold text-slate-950">
                {totalOpportunities.toLocaleString(
                  "en-IN"
                )}
              </p>

              <p className="text-xs text-slate-400">
                total opportunities
              </p>

            </div>

          </div>

          {totalCategories === 0 ? (
            <div className="flex min-h-[220px] items-center justify-center text-center">

              <div>

                <Target className="mx-auto h-8 w-8 text-slate-300" />

                <p className="mt-3 text-sm font-medium text-slate-600">
                  No opportunities detected
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  Try uploading a dataset with
                  supported revenue/payment columns.
                </p>

              </div>

            </div>
          ) : (
            <div className="mt-8 space-y-7">

              {/* Recover */}
              <div>

                <div className="mb-2 flex justify-between">

                  <span className="text-sm font-medium text-slate-700">
                    Recover
                  </span>

                  <span className="text-sm font-semibold text-slate-950">
                    {recoverCount}{" "}
                    <span className="font-normal text-slate-400">
                      ({recoverPercentage.toFixed(1)}%)
                    </span>
                  </span>

                </div>

                <div className="h-3 overflow-hidden rounded-full bg-slate-100">

                  <div
                    className="h-full rounded-full bg-blue-500 transition-all duration-500"
                    style={{
                      width: `${recoverPercentage}%`,
                    }}
                  />

                </div>

              </div>

              {/* Prevent */}
              <div>

                <div className="mb-2 flex justify-between">

                  <span className="text-sm font-medium text-slate-700">
                    Prevent
                  </span>

                  <span className="text-sm font-semibold text-slate-950">
                    {preventCount}{" "}
                    <span className="font-normal text-slate-400">
                      ({preventPercentage.toFixed(1)}%)
                    </span>
                  </span>

                </div>

                <div className="h-3 overflow-hidden rounded-full bg-slate-100">

                  <div
                    className="h-full rounded-full bg-violet-500 transition-all duration-500"
                    style={{
                      width: `${preventPercentage}%`,
                    }}
                  />

                </div>

              </div>

              {/* Grow */}
              <div>

                <div className="mb-2 flex justify-between">

                  <span className="text-sm font-medium text-slate-700">
                    Grow
                  </span>

                  <span className="text-sm font-semibold text-slate-950">
                    {growCount}{" "}
                    <span className="font-normal text-slate-400">
                      ({growPercentage.toFixed(1)}%)
                    </span>
                  </span>

                </div>

                <div className="h-3 overflow-hidden rounded-full bg-slate-100">

                  <div
                    className="h-full rounded-full bg-emerald-500 transition-all duration-500"
                    style={{
                      width: `${growPercentage}%`,
                    }}
                  />

                </div>

              </div>

            </div>
          )}

        </Card>

        {/* DATASET SUMMARY */}
        <Card className="p-7">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50 text-[#146ef5]">
              <Target className="h-5 w-5" />
            </div>

            <div>
              <h2 className="font-semibold text-slate-950">
                Dataset analysis
              </h2>

              <p className="text-xs text-slate-400">
                Results generated from your uploaded data
              </p>
            </div>

          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            {/* Dataset */}
            <div className="rounded-xl bg-slate-50 p-4">

              <p className="text-xs text-slate-400">
                Dataset
              </p>

              <p className="mt-1 truncate text-sm font-semibold text-slate-800">
                {datasetFilename}
              </p>

            </div>

            {/* Rows */}
            <div className="rounded-xl bg-slate-50 p-4">

              <p className="text-xs text-slate-400">
                Rows
              </p>

              <p className="mt-1 text-lg font-semibold text-slate-800">
                {datasetRows.toLocaleString(
                  "en-IN"
                )}
              </p>

            </div>

            {/* Columns */}
            <div className="rounded-xl bg-slate-50 p-4">

              <p className="text-xs text-slate-400">
                Columns
              </p>

              <p className="mt-1 text-lg font-semibold text-slate-800">
                {datasetColumns.toLocaleString(
                  "en-IN"
                )}
              </p>

            </div>

            {/* Opportunities */}
            <div className="rounded-xl bg-slate-50 p-4">

              <p className="text-xs text-slate-400">
                Opportunities
              </p>

              <p className="mt-1 text-lg font-semibold text-slate-800">
                {totalOpportunities.toLocaleString(
                  "en-IN"
                )}
              </p>

            </div>

          </div>

        </Card>

      </div>
    </DashboardLayout>
  );
}