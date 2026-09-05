"use client";

import { useRef, useState } from "react";
import {
  UploadCloud,
  FileSpreadsheet,
  X,
} from "lucide-react";
import { Button } from "../ui/Button";

interface UploadDropzoneProps {
  onFileSelected: (file: File) => void;
  loading?: boolean;
}

const extensions = [
  ".csv",
  ".xlsx",
  ".xls",
  ".json",
];

export function UploadDropzone({
  onFileSelected,
  loading = false,
}: UploadDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const [dragging, setDragging] =
    useState(false);

  const [selectedFile, setSelectedFile] =
    useState<File | null>(null);

  function handleFile(file?: File) {
    if (!file) return;

    const valid =
      extensions.some((ext) =>
        file.name.toLowerCase().endsWith(ext)
      );

    if (!valid) {
      alert(
        "Please upload CSV, XLS, XLSX or JSON."
      );
      return;
    }

    setSelectedFile(file);
    onFileSelected(file);
  }

  return (
    <div>
      <div
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragging(false);

          handleFile(event.dataTransfer.files[0]);
        }}
        className={`rounded-3xl border-2 border-dashed p-12 text-center transition ${
          dragging
            ? "border-[#146ef5] bg-blue-50"
            : "border-slate-200 bg-white hover:border-slate-300"
        }`}
      >
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-50 text-[#146ef5]">
          <UploadCloud size={30} />
        </div>

        <h3 className="mt-5 text-lg font-semibold text-slate-950">
          Drop your dataset here
        </h3>

        <p className="mt-2 text-sm text-slate-500">
          or choose a file from your computer
        </p>

        <div className="mt-6">
          <Button
            type="button"
            disabled={loading}
            onClick={() =>
              inputRef.current?.click()
            }
          >
            <FileSpreadsheet
              size={17}
              className="mr-2"
            />

            Choose Dataset
          </Button>
        </div>

        <p className="mt-5 text-xs text-slate-400">
          CSV · XLSX · XLS · JSON
        </p>

        <input
          ref={inputRef}
          type="file"
          accept=".csv,.xlsx,.xls,.json"
          className="hidden"
          onChange={(event) =>
            handleFile(event.target.files?.[0])
          }
        />
      </div>

      {selectedFile && (
        <div className="mt-4 flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4">
          <div className="flex items-center gap-3">
            <FileSpreadsheet
              size={20}
              className="text-[#146ef5]"
            />

            <div>
              <p className="text-sm font-semibold text-slate-900">
                {selectedFile.name}
              </p>

              <p className="text-xs text-slate-400">
                {(selectedFile.size / 1024 / 1024).toFixed(
                  2
                )}{" "}
                MB
              </p>
            </div>
          </div>

          <button
            onClick={() => setSelectedFile(null)}
            className="rounded-lg p-2 hover:bg-slate-100"
          >
            <X size={17} />
          </button>
        </div>
      )}
    </div>
  );
}