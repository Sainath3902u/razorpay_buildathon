"use client";

import { useRouter } from "next/navigation";
import { Database, Sparkles } from "lucide-react";

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

  const { saveDataset } = useDataset();

  async function handleFile(file: File) {
    const response = await upload(file);

    const capabilities = Array.isArray(
      response.capabilities
    )
      ? response.capabilities.map(String)
      : Object.keys(
          response.capabilities || {}
        );

    saveDataset({
      datasetId: response.dataset_id,
      filename: response.filename,
      rows: response.rows,
      columns: response.columns,
      capabilities,
      columnMapping:
        response.column_mapping || {},
    });
  }

  return (
    <DashboardLayout>
      <div className="mx-auto max-w-4xl">
        <div className="mb-8">
          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-[#146ef5]">
            <Database size={23} />
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-slate-950">
            Upload your payment data
          </h1>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            Connect your transaction dataset and let RevenueOS
            identify actionable revenue opportunities.
          </p>
        </div>

        <UploadDropzone
          onFileSelected={handleFile}
          loading={loading}
        />

        {loading && <UploadProgress />}

        {error && (
          <div className="mt-6 rounded-2xl border border-red-100 bg-red-50 p-5">
            <p className="text-sm font-semibold text-red-700">
              Upload failed
            </p>

            <p className="mt-1 text-sm text-red-600">
              {error}
            </p>
          </div>
        )}

        {result && (
          <DatasetSummary
            result={result}
            onContinue={() =>
              router.push("/dashboard")
            }
          />
        )}

        {!result && !loading && (
          <div className="mt-8 grid gap-4 md:grid-cols-3">
            {[
              [
                "1",
                "Upload",
                "Drop your transaction dataset.",
              ],
              [
                "2",
                "Analyze",
                "Our engine detects revenue signals.",
              ],
              [
                "3",
                "Act",
                "Prioritize the highest-value actions.",
              ],
            ].map(([number, title, text]) => (
              <div
                key={number}
                className="rounded-2xl border border-slate-200 bg-white p-5"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 text-sm font-bold">
                  {number}
                </div>

                <h3 className="mt-4 font-semibold text-slate-950">
                  {title}
                </h3>

                <p className="mt-1 text-xs leading-5 text-slate-400">
                  {text}
                </p>
              </div>
            ))}
          </div>
        )}

        <div className="mt-8 flex items-center gap-2 text-xs text-slate-400">
          <Sparkles size={14} />
          Supported: CSV, Excel and JSON
        </div>
      </div>
    </DashboardLayout>
  );
}