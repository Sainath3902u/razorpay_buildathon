import { LoaderCircle } from "lucide-react";

export function UploadProgress() {
  return (
    <div className="mt-6 rounded-2xl border border-blue-100 bg-blue-50 p-5">
      <div className="flex items-center gap-3">
        <LoaderCircle
          size={20}
          className="animate-spin text-[#146ef5]"
        />

        <div>
          <p className="text-sm font-semibold text-blue-900">
            Analyzing dataset...
          </p>

          <p className="mt-1 text-xs text-blue-600">
            Detecting schema and normalizing your data.
          </p>
        </div>
      </div>
    </div>
  );
}