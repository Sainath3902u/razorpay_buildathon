"use client";

import { Card } from "../ui/Card";

const values = [
  34, 42, 38, 55, 48, 62, 58, 71, 65, 76, 70, 84,
];

export function RevenueChart() {
  return (
    <Card className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="font-semibold text-slate-950">
            Revenue exposure
          </h2>

          <p className="mt-1 text-xs text-slate-400">
            Expected revenue opportunity over time
          </p>
        </div>

        <select className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs text-slate-600 outline-none">
          <option>Last 12 months</option>
          <option>Last 6 months</option>
          <option>Last 30 days</option>
        </select>
      </div>

      <div className="flex h-64 items-end gap-2">
        {values.map((value, index) => (
          <div
            key={index}
            className="group relative flex h-full flex-1 items-end"
          >
            <div
              className="w-full rounded-t-lg bg-[#146ef5] opacity-80 transition group-hover:opacity-100"
              style={{
                height: `${value}%`,
              }}
            />
          </div>
        ))}
      </div>

      <div className="mt-3 flex justify-between text-[10px] text-slate-400">
        <span>Oct</span>
        <span>Nov</span>
        <span>Dec</span>
        <span>Jan</span>
        <span>Feb</span>
        <span>Mar</span>
        <span>Apr</span>
        <span>May</span>
        <span>Jun</span>
        <span>Jul</span>
        <span>Aug</span>
        <span>Sep</span>
      </div>
    </Card>
  );
}