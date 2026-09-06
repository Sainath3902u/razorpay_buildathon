// "use client";

// import { useMemo, useState } from "react";
// import {
//   Target,
//   AlertCircle,
//   Search,
// } from "lucide-react";

// import { DashboardLayout } from "@/components/layout/DashboardLayout";
// import { OpportunityFilters } from "@/components/opportunities/OpportunityFilters";
// import { OpportunityTable } from "@/components/opportunities/OpportunityTable";
// import { OpportunityCard } from "@/components/opportunities/OpportunityCard";
// import { OpportunityDetails } from "@/components/opportunities/OpportunityDetails";
// import { OpportunityAIChat } from "@/components/opportunities/OpportunityAIChat";
// import { Modal } from "@/components/ui/Modal";

// import { useDataset } from "@/hooks/useDataset";
// import { useOpportunities } from "@/hooks/useOpportunities";

// import { Opportunity } from "@/types/opportunity";

// export default function OpportunitiesPage() {
//   const { dataset } = useDataset();

//   const datasetId = dataset?.datasetId ?? null;

//   const {
//     opportunities,
//     loading,
//     error,
//   } = useOpportunities(datasetId);

//   const [category, setCategory] =
//     useState("ALL");

//   const [priority, setPriority] =
//     useState("ALL");

//   const [search, setSearch] =
//     useState("");

//   const [selected, setSelected] =
//     useState<Opportunity | null>(null);

//   /*
//    * -----------------------------------------
//    * FILTER OPPORTUNITIES
//    * -----------------------------------------
//    */

//   const filtered = useMemo(() => {
//     const query = search
//       .toLowerCase()
//       .trim();

//     return opportunities.filter((item) => {
//       const categoryMatch =
//         category === "ALL" ||
//         item.category === category;

//       const priorityMatch =
//         priority === "ALL" ||
//         item.priority === priority;

//       const opportunityType =
//         item.opportunity_type
//           ?.toLowerCase() ?? "";

//       const customerId =
//         item.customer_id
//           ?.toLowerCase() ?? "";

//       const opportunityId =
//         item.opportunity_id
//           ?.toLowerCase() ?? "";

//       const reason =
//         item.reason
//           ?.toLowerCase() ?? "";

//       const searchMatch =
//         !query ||
//         opportunityType.includes(query) ||
//         customerId.includes(query) ||
//         opportunityId.includes(query) ||
//         reason.includes(query);

//       return (
//         categoryMatch &&
//         priorityMatch &&
//         searchMatch
//       );
//     });
//   }, [
//     opportunities,
//     category,
//     priority,
//     search,
//   ]);

//   /*
//    * -----------------------------------------
//    * COUNTS
//    * -----------------------------------------
//    */

//   const totalCount =
//     opportunities.length;

//   const filteredCount =
//     filtered.length;

//   /*
//    * -----------------------------------------
//    * PAGE
//    * -----------------------------------------
//    */

//   return (
//     <DashboardLayout>
//       <div className="space-y-6">

//         {/* Header */}
//         <section>

//           <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-[#146ef5]">
//             <Target size={23} />
//           </div>

//           <h1 className="mt-4 text-3xl font-bold tracking-tight text-slate-950">
//             Revenue opportunities
//           </h1>

//           <p className="mt-2 text-sm text-slate-500">
//             Opportunities generated from your uploaded dataset.
//           </p>

//           {dataset?.filename && (
//             <p className="mt-2 text-xs text-slate-400">
//               Dataset:{" "}
//               <span className="font-medium text-slate-500">
//                 {dataset.filename}
//               </span>
//             </p>
//           )}

//         </section>

//         {/* No dataset */}
//         {!datasetId && (
//           <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">

//             <div className="flex items-start gap-3">

//               <AlertCircle
//                 size={18}
//                 className="mt-0.5 text-amber-600"
//               />

//               <div>

//                 <p className="text-sm font-semibold text-amber-800">
//                   No dataset selected
//                 </p>

//                 <p className="mt-1 text-sm text-amber-700">
//                   Upload a dataset first to generate
//                   revenue opportunities.
//                 </p>

//               </div>

//             </div>

//           </div>
//         )}

//         {/* Backend error */}
//         {error && (
//           <div className="flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 p-5">

//             <AlertCircle
//               size={18}
//               className="mt-0.5 shrink-0 text-red-600"
//             />

//             <div>

//               <p className="text-sm font-semibold text-red-800">
//                 Unable to load opportunities
//               </p>

//               <p className="mt-1 text-sm text-red-700">
//                 {error}
//               </p>

//             </div>

//           </div>
//         )}

//         {/* Loading */}
//         {loading && (
//           <div className="rounded-2xl border border-slate-200 bg-white p-5 text-sm text-slate-500">
//             Loading backend analysis...
//           </div>
//         )}

//         {/* No opportunities */}
//         {datasetId &&
//           !loading &&
//           !error &&
//           opportunities.length === 0 && (
//             <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center">

//               <Target
//                 size={30}
//                 className="mx-auto text-slate-300"
//               />

//               <p className="mt-4 font-semibold text-slate-900">
//                 No opportunities detected
//               </p>

//               <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-slate-500">
//                 The dataset was processed successfully,
//                 but none of the detectors found a
//                 qualifying revenue signal.
//               </p>

//             </div>
//           )}

//         {/* Opportunities */}
//         {opportunities.length > 0 && (
//           <>
//             {/* Filters */}
//             <OpportunityFilters
//               category={category}
//               priority={priority}
//               search={search}
//               onCategoryChange={setCategory}
//               onPriorityChange={setPriority}
//               onSearchChange={setSearch}
//             />

//             {/* Result summary */}
//             <div className="flex items-center justify-between text-sm text-slate-400">

//               <span>
//                 Showing{" "}
//                 <span className="font-medium text-slate-600">
//                   {filteredCount}
//                 </span>{" "}
//                 of{" "}
//                 <span className="font-medium text-slate-600">
//                   {totalCount}
//                 </span>{" "}
//                 opportunities
//               </span>

//               {search && (
//                 <button
//                   type="button"
//                   onClick={() => setSearch("")}
//                   className="text-[#146ef5] hover:underline"
//                 >
//                   Clear search
//                 </button>
//               )}

//             </div>

//             {/* Desktop table */}
//             <div className="hidden lg:block">

//               {filtered.length > 0 ? (
//                 <OpportunityTable
//                   opportunities={filtered}
//                   onSelect={setSelected}
//                 />
//               ) : (
//                 <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center">

//                   <Search
//                     size={28}
//                     className="mx-auto text-slate-300"
//                   />

//                   <p className="mt-4 font-semibold text-slate-900">
//                     No matching opportunities
//                   </p>

//                   <p className="mt-2 text-sm text-slate-500">
//                     Try changing your category,
//                     priority, or search filters.
//                   </p>

//                 </div>
//               )}

//             </div>

//             {/* Mobile cards */}
//             <div className="grid gap-4 lg:hidden">

//               {filtered.length > 0 ? (
//                 filtered.map((item) => (
//                   <OpportunityCard
//                     key={item.opportunity_id}
//                     opportunity={item}
//                     onClick={() =>
//                       setSelected(item)
//                     }
//                   />
//                 ))
//               ) : (
//                 <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center">

//                   <Search
//                     size={28}
//                     className="mx-auto text-slate-300"
//                   />

//                   <p className="mt-4 font-semibold text-slate-900">
//                     No matching opportunities
//                   </p>

//                   <p className="mt-2 text-sm text-slate-500">
//                     Try changing your filters.
//                   </p>

//                 </div>
//               )}

//             </div>
//           </>
//         )}

//         Opportunity details modal
//         <Modal
//           open={Boolean(selected)}
//           title="Opportunity details"
//           onClose={() =>
//             setSelected(null)
//           }
//         >
//           {selected && (
//             <OpportunityDetails
//               opportunity={selected}
//             />
//           )}
//         </Modal>

//       </div>
//     </DashboardLayout>
//   );
// }



"use client";

import { useMemo, useState } from "react";

import {
  Target,
  AlertCircle,
  Search,
} from "lucide-react";

import { DashboardLayout } from "@/components/layout/DashboardLayout";

import { OpportunityFilters } from "@/components/opportunities/OpportunityFilters";
import { OpportunityTable } from "@/components/opportunities/OpportunityTable";
import { OpportunityCard } from "@/components/opportunities/OpportunityCard";
import { OpportunityDetails } from "@/components/opportunities/OpportunityDetails";
import { OpportunityAIChat } from "@/components/opportunities/OpportunityAIChat";

import { Modal } from "@/components/ui/Modal";

import { useDataset } from "@/hooks/useDataset";
import { useOpportunities } from "@/hooks/useOpportunities";

import { Opportunity } from "@/types/opportunity";

export default function OpportunitiesPage() {
  const { dataset } = useDataset();

  const datasetId = dataset?.datasetId ?? null;

  const {
    opportunities,
    loading,
    error,
  } = useOpportunities(datasetId);

  /*
   * -----------------------------------------
   * FILTER STATE
   * -----------------------------------------
   */

  const [category, setCategory] =
    useState("ALL");

  const [priority, setPriority] =
    useState("ALL");

  const [search, setSearch] =
    useState("");

  /*
   * Selected opportunity for details modal
   */
  const [selected, setSelected] =
    useState<Opportunity | null>(null);

  /*
   * Selected opportunity for AI chatbot
   */
  const [aiOpportunity, setAiOpportunity] =
    useState<Opportunity | null>(null);

  /*
   * -----------------------------------------
   * OPEN OPPORTUNITY
   * -----------------------------------------
   *
   * Whenever an opportunity is clicked:
   * - open details modal
   * - open AI assistant
   *
   */

  const handleOpportunitySelect = (
    opportunity: Opportunity
  ) => {
    setSelected(opportunity);
    setAiOpportunity(opportunity);
  };

  /*
   * -----------------------------------------
   * FILTER OPPORTUNITIES
   * -----------------------------------------
   */

  const filtered = useMemo(() => {
    const query = search
      .toLowerCase()
      .trim();

    return opportunities.filter((item) => {
      const categoryMatch =
        category === "ALL" ||
        item.category === category;

      const priorityMatch =
        priority === "ALL" ||
        item.priority === priority;

      const opportunityType =
        item.opportunity_type
          ?.toLowerCase() ?? "";

      const customerId =
        item.customer_id
          ?.toLowerCase() ?? "";

      const opportunityId =
        item.opportunity_id
          ?.toLowerCase() ?? "";

      const reason =
        item.reason
          ?.toLowerCase() ?? "";

      const searchMatch =
        !query ||
        opportunityType.includes(query) ||
        customerId.includes(query) ||
        opportunityId.includes(query) ||
        reason.includes(query);

      return (
        categoryMatch &&
        priorityMatch &&
        searchMatch
      );
    });
  }, [
    opportunities,
    category,
    priority,
    search,
  ]);

  /*
   * -----------------------------------------
   * COUNTS
   * -----------------------------------------
   */

  const totalCount =
    opportunities.length;

  const filteredCount =
    filtered.length;

  /*
   * -----------------------------------------
   * PAGE
   * -----------------------------------------
   */

  return (
    <DashboardLayout>
      <div className="space-y-6">

        {/* ================================
            HEADER
        ================================= */}

        <section>

          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-[#146ef5]">
            <Target size={23} />
          </div>

          <h1 className="mt-4 text-3xl font-bold tracking-tight text-slate-950">
            Revenue opportunities
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Opportunities generated from your uploaded dataset.
          </p>

          {dataset?.filename && (
            <p className="mt-2 text-xs text-slate-400">
              Dataset:{" "}
              <span className="font-medium text-slate-500">
                {dataset.filename}
              </span>
            </p>
          )}

        </section>

        {/* ================================
            NO DATASET
        ================================= */}

        {!datasetId && (
          <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">

            <div className="flex items-start gap-3">

              <AlertCircle
                size={18}
                className="mt-0.5 text-amber-600"
              />

              <div>

                <p className="text-sm font-semibold text-amber-800">
                  No dataset selected
                </p>

                <p className="mt-1 text-sm text-amber-700">
                  Upload a dataset first to generate
                  revenue opportunities.
                </p>

              </div>

            </div>

          </div>
        )}

        {/* ================================
            BACKEND ERROR
        ================================= */}

        {error && (
          <div className="flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 p-5">

            <AlertCircle
              size={18}
              className="mt-0.5 shrink-0 text-red-600"
            />

            <div>

              <p className="text-sm font-semibold text-red-800">
                Unable to load opportunities
              </p>

              <p className="mt-1 text-sm text-red-700">
                {error}
              </p>

            </div>

          </div>
        )}

        {/* ================================
            LOADING
        ================================= */}

        {loading && (
          <div className="rounded-2xl border border-slate-200 bg-white p-5 text-sm text-slate-500">
            Loading backend analysis...
          </div>
        )}

        {/* ================================
            NO OPPORTUNITIES
        ================================= */}

        {datasetId &&
          !loading &&
          !error &&
          opportunities.length === 0 && (
            <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center">

              <Target
                size={30}
                className="mx-auto text-slate-300"
              />

              <p className="mt-4 font-semibold text-slate-900">
                No opportunities detected
              </p>

              <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-slate-500">
                The dataset was processed successfully,
                but none of the detectors found a
                qualifying revenue signal.
              </p>

            </div>
          )}

        {/* ================================
            OPPORTUNITIES
        ================================= */}

        {opportunities.length > 0 && (
          <>

            {/* Filters */}
            <OpportunityFilters
              category={category}
              priority={priority}
              search={search}
              onCategoryChange={setCategory}
              onPriorityChange={setPriority}
              onSearchChange={setSearch}
            />

            {/* Result summary */}
            <div className="flex items-center justify-between text-sm text-slate-400">

              <span>
                Showing{" "}
                <span className="font-medium text-slate-600">
                  {filteredCount}
                </span>{" "}
                of{" "}
                <span className="font-medium text-slate-600">
                  {totalCount}
                </span>{" "}
                opportunities
              </span>

              {search && (
                <button
                  type="button"
                  onClick={() => setSearch("")}
                  className="text-[#146ef5] hover:underline"
                >
                  Clear search
                </button>
              )}

            </div>

            {/* ============================
                DESKTOP TABLE
            ============================= */}

            <div className="hidden lg:block">

              {filtered.length > 0 ? (
                <OpportunityTable
                  opportunities={filtered}
                  onSelect={
                    handleOpportunitySelect
                  }
                />
              ) : (
                <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center">

                  <Search
                    size={28}
                    className="mx-auto text-slate-300"
                  />

                  <p className="mt-4 font-semibold text-slate-900">
                    No matching opportunities
                  </p>

                  <p className="mt-2 text-sm text-slate-500">
                    Try changing your category,
                    priority, or search filters.
                  </p>

                </div>
              )}

            </div>

            {/* ============================
                MOBILE CARDS
            ============================= */}

            <div className="grid gap-4 lg:hidden">

              {filtered.length > 0 ? (
                filtered.map((item) => (
                  <OpportunityCard
                    key={item.opportunity_id}
                    opportunity={item}
                    onClick={() =>
                      handleOpportunitySelect(
                        item
                      )
                    }
                  />
                ))
              ) : (
                <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center">

                  <Search
                    size={28}
                    className="mx-auto text-slate-300"
                  />

                  <p className="mt-4 font-semibold text-slate-900">
                    No matching opportunities
                  </p>

                  <p className="mt-2 text-sm text-slate-500">
                    Try changing your filters.
                  </p>

                </div>
              )}

            </div>

          </>
        )}

        {/* ================================
            OPPORTUNITY DETAILS
        ================================= */}

        <Modal
          open={Boolean(selected)}
          title="Opportunity details"
          onClose={() => setSelected(null)}
          className={
            aiOpportunity
              ? "lg:mr-[28rem]"
              : ""
          }
        >
          {selected && (
            <OpportunityDetails
              opportunity={selected}
            />
          )}
        </Modal>

        {/* ================================
            AI CHATBOT
        ================================= */}

        <OpportunityAIChat
          opportunity={aiOpportunity}
          onClose={() =>
            setAiOpportunity(null)
          }
        />

      </div>
    </DashboardLayout>
  );
}