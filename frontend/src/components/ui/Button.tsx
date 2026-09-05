import { ButtonHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
}

export function Button({
  variant = "primary",
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-xl px-4 py-2.5 text-sm font-semibold transition",
        "disabled:cursor-not-allowed disabled:opacity-50",

        variant === "primary" &&
          "bg-[#146ef5] text-white hover:bg-[#0f5ed8]",

        variant === "secondary" &&
          "border border-slate-200 bg-white text-slate-900 hover:bg-slate-50",

        variant === "ghost" &&
          "text-slate-600 hover:bg-slate-100",

        className
      )}
      {...props}
    />
  );
}