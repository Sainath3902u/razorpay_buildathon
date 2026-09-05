"use client";

interface Props {
  category: string;
  priority: string;
  search: string;
  onCategoryChange: (value: string) => void;
  onPriorityChange: (value: string) => void;
  onSearchChange: (value: string) => void;
}

export function OpportunityFilters({
  category,
  priority,
  search,
  onCategoryChange,
  onPriorityChange,
  onSearchChange,
}: Props) {
  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 md:flex-row">
      <input
        value={search}
        onChange={(e) =>
          onSearchChange(e.target.value)
        }
        placeholder="Search customer or opportunity..."
        className="flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm outline-none focus:border-blue-400 focus:bg-white"
      />

      <select
        value={category}
        onChange={(e) =>
          onCategoryChange(e.target.value)
        }
        className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm"
      >
        <option value="ALL">All categories</option>
        <option value="RECOVER">Recover</option>
        <option value="PREVENT">Prevent</option>
        <option value="GROW">Grow</option>
      </select>

      <select
        value={priority}
        onChange={(e) =>
          onPriorityChange(e.target.value)
        }
        className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm"
      >
        <option value="ALL">All priorities</option>
        <option value="HIGH">High</option>
        <option value="MEDIUM">Medium</option>
        <option value="LOW">Low</option>
      </select>
    </div>
  );
}