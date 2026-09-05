"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Upload,
  Target,
  BarChart3,
  Sparkles,
  ChevronRight,
} from "lucide-react";

const items = [
  {
    label: "Overview",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "Upload Dataset",
    href: "/upload",
    icon: Upload,
  },
  {
    label: "Opportunities",
    href: "/opportunities",
    icon: Target,
  },
  {
    label: "Analytics",
    href: "/analytics",
    icon: BarChart3,
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-40 hidden h-screen w-64 border-r border-slate-200 bg-white lg:block">
      <div className="flex h-full flex-col">
        <div className="flex h-20 items-center gap-3 border-b border-slate-100 px-6">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#146ef5] text-white">
            <Sparkles size={19} />
          </div>

          <div>
            <div className="font-bold tracking-tight text-slate-950">
              RevenueOS
            </div>

            <div className="text-[10px] font-medium uppercase tracking-wider text-slate-400">
              Intelligence
            </div>
          </div>
        </div>

        <nav className="flex-1 space-y-1 p-4">
          {items.map((item) => {
            const Icon = item.icon;

            const active =
              pathname === item.href ||
              pathname.startsWith(`${item.href}/`);

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                  active
                    ? "bg-blue-50 text-[#146ef5]"
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-950"
                }`}
              >
                <Icon size={18} />

                <span>{item.label}</span>

                {active && (
                  <ChevronRight
                    size={15}
                    className="ml-auto"
                  />
                )}
              </Link>
            );
          })}
        </nav>

        <div className="m-4 rounded-2xl bg-slate-950 p-4 text-white">
          <div className="mb-2 flex items-center gap-2">
            <Sparkles size={16} />

            <span className="text-sm font-semibold">
              AI Intelligence
            </span>
          </div>

          <p className="text-xs leading-5 text-slate-400">
            Turn payment signals into revenue actions.
          </p>
        </div>
      </div>
    </aside>
  );
}