"use client";

import {
  Bell,
  Search,
  Menu,
} from "lucide-react";

export function Topbar() {
  return (
    <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200 bg-white/90 px-5 backdrop-blur lg:px-8">
      <button className="rounded-lg p-2 hover:bg-slate-100 lg:hidden">
        <Menu size={20} />
      </button>

      <div className="hidden max-w-md flex-1 lg:block">
        <div className="relative">
          <Search
            size={17}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <input
            placeholder="Search customers, opportunities..."
            className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-4 text-sm outline-none focus:border-blue-400 focus:bg-white"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700 sm:flex">
          <span className="h-2 w-2 rounded-full bg-emerald-500" />
          API Connected
        </div>

        <button className="rounded-xl p-2.5 text-slate-500 hover:bg-slate-100">
          <Bell size={19} />
        </button>

        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-sm font-bold text-white">
          S
        </div>
      </div>
    </header>
  );
}