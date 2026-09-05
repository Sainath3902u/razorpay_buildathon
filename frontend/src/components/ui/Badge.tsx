import { cn } from "@/lib/utils";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "high" | "medium" | "low" | "blue" | "green";
}

export function Badge({
  children,
  variant = "blue",
}: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-1 text-xs font-semibold",

        variant === "high" &&
          "bg-red-50 text-red-600",

        variant === "medium" &&
          "bg-amber-50 text-amber-700",

        variant === "low" &&
          "bg-slate-100 text-slate-600",

        variant === "blue" &&
          "bg-blue-50 text-blue-600",

        variant === "green" &&
          "bg-emerald-50 text-emerald-600"
      )}
    >
      {children}
    </span>
  );
}