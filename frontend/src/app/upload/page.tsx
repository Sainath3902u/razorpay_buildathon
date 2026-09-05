"use client";

import { useRouter } from "next/navigation";
import {
  Database,
  Sparkles,
  Target,
  IndianRupee,
  ShieldCheck,
} from "lucide-react";

import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { UploadDropzone } from "@/components/upload/UploadDropzone";
import { UploadProgress } from "@/components/upload/UploadProgress";
import { DatasetSummary } from "@/components/upload/DatasetSummary";
import { useUpload } from "@/hooks/useUpload";
import { useDataset } from "@/hooks/useDataset";


export default function UploadPage() {

  const router = useRouter();

  const {
    upload,
    loading,
    result,
    error,
  } = useUpload();

  const {
    saveDataset,
  } = useDataset();


  async function handleFile(
    file: File
  ) {

    try {

      const response =
        await upload(file);

      const capabilities =
        Array.isArray(
          response.capabilities
        )
          ? response.capabilities.map(String)
          : Object.entries(
              response.capabilities || {}
            )
              .filter(
                ([, value]) =>
                  Boolean(value)
              )
              .map(
                ([key]) => key
              );


      saveDataset({

        datasetId:
          response.dataset_id,

        filename:
          response.filename,

        rows:
          response.rows,

        columns:
          response.columns,

        capabilities,

        columnMapping:
          response.column_mapping || {},

        summary:
          response.summary,

      });

    } catch {
      // Error is already shown by useUpload.
    }
  }


  return (
    <DashboardLayout>

      <div className="mx-auto max-w-5xl">

        <div className="mb-8">

          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-[#146ef5]">
            <Database size={23} />
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-slate-950">
            Upload your payment data
          </h1>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            Upload your transaction dataset and let RevenueOS
            detect recover, prevent and growth opportunities.
          </p>

        </div>


        <UploadDropzone
          onFileSelected={handleFile}
          loading={loading}
        />


        {loading && (
          <UploadProgress />
        )}


        {error && (

          <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-5">

            <p className="text-sm font-semibold text-red-800">
              Dataset processing failed
            </p>

            <p className="mt-2 text-sm leading-6 text-red-700">
              {error}
            </p>

            <p className="mt-3 text-xs text-red-600">
              Check the FastAPI terminal for the full backend error.
            </p>

          </div>

        )}


        {result && (

          <div className="mt-8 space-y-6">

            <DatasetSummary
              result={result}
              onContinue={() =>
                router.push("/dashboard")
              }
            />


            <div className="grid gap-4 md:grid-cols-3">

              <div className="rounded-2xl border border-slate-200 bg-white p-5">

                <div className="flex items-center gap-3">

                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-[#146ef5]">
                    <IndianRupee size={18} />
                  </div>

                  <div>
                    <p className="text-xs text-slate-400">
                      Revenue at risk
                    </p>

                    <p className="text-xl font-bold text-slate-950">
                      ₹{result.summary.total_amount_at_risk.toLocaleString("en-IN")}
                    </p>
                  </div>

                </div>

              </div>


              <div className="rounded-2xl border border-slate-200 bg-white p-5">

                <div className="flex items-center gap-3">

                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
                    <Target size={18} />
                  </div>

                  <div>
                    <p className="text-xs text-slate-400">
                      Expected value
                    </p>

                    <p className="text-xl font-bold text-slate-950">
                      ₹{result.summary.total_expected_value.toLocaleString("en-IN")}
                    </p>
                  </div>

                </div>

              </div>


              <div className="rounded-2xl border border-slate-200 bg-white p-5">

                <div className="flex items-center gap-3">

                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-50 text-violet-600">
                    <ShieldCheck size={18} />
                  </div>

                  <div>
                    <p className="text-xs text-slate-400">
                      Opportunities
                    </p>

                    <p className="text-xl font-bold text-slate-950">
                      {result.summary.total_opportunities}
                    </p>
                  </div>

                </div>

              </div>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-white p-6">

              <div className="flex items-center gap-2">

                <Sparkles
                  size={18}
                  className="text-[#146ef5]"
                />

                <h2 className="font-semibold text-slate-950">
                  Analysis completed
                </h2>

              </div>


              <div className="mt-5 grid gap-4 sm:grid-cols-3">

                <div className="rounded-xl bg-slate-50 p-4">

                  <p className="text-xs text-slate-400">
                    Recover
                  </p>

                  <p className="mt-1 text-2xl font-bold">
                    {result.summary.category_counts.RECOVER}
                  </p>

                </div>


                <div className="rounded-xl bg-slate-50 p-4">

                  <p className="text-xs text-slate-400">
                    Prevent
                  </p>

                  <p className="mt-1 text-2xl font-bold">
                    {result.summary.category_counts.PREVENT}
                  </p>

                </div>


                <div className="rounded-xl bg-slate-50 p-4">

                  <p className="text-xs text-slate-400">
                    Grow
                  </p>

                  <p className="mt-1 text-2xl font-bold">
                    {result.summary.category_counts.GROW}
                  </p>

                </div>

              </div>

            </div>

          </div>

        )}


        {!result &&
          !loading &&
          !error && (

            <div className="mt-8 grid gap-4 md:grid-cols-3">

              <div className="rounded-2xl border border-slate-200 bg-white p-5">

                <p className="text-xs font-bold text-[#146ef5]">
                  01
                </p>

                <h3 className="mt-4 font-semibold">
                  Upload
                </h3>

                <p className="mt-1 text-xs leading-5 text-slate-400">
                  Drop your transaction dataset.
                </p>

              </div>


              <div className="rounded-2xl border border-slate-200 bg-white p-5">

                <p className="text-xs font-bold text-[#146ef5]">
                  02
                </p>

                <h3 className="mt-4 font-semibold">
                  Analyze
                </h3>

                <p className="mt-1 text-xs leading-5 text-slate-400">
                  Run the backend opportunity detectors.
                </p>

              </div>


              <div className="rounded-2xl border border-slate-200 bg-white p-5">

                <p className="text-xs font-bold text-[#146ef5]">
                  03
                </p>

                <h3 className="mt-4 font-semibold">
                  Act
                </h3>

                <p className="mt-1 text-xs leading-5 text-slate-400">
                  Review the highest-value opportunities.
                </p>

              </div>

            </div>

          )}


        <div className="mt-8 flex items-center gap-2 text-xs text-slate-400">

          <Sparkles size={14} />

          Supported: CSV, XLSX, XLS and JSON

        </div>

      </div>

    </DashboardLayout>
  );
}