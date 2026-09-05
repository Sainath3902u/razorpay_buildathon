import { Card } from "../ui/Card";

export function OpportunitySummary() {
  const data = [
    {
      label: "Recover",
      value: 124,
      percentage: 50,
      className: "bg-blue-500",
    },
    {
      label: "Prevent",
      value: 71,
      percentage: 29,
      className: "bg-violet-500",
    },
    {
      label: "Grow",
      value: 52,
      percentage: 21,
      className: "bg-emerald-500",
    },
  ];

  return (
    <Card className="p-6">
      <div>
        <h2 className="font-semibold text-slate-950">
          Opportunity mix
        </h2>

        <p className="mt-1 text-xs text-slate-400">
          Distribution across revenue actions
        </p>
      </div>

      <div className="mt-6 space-y-5">
        {data.map((item) => (
          <div key={item.label}>
            <div className="mb-2 flex justify-between text-sm">
              <span className="font-medium text-slate-700">
                {item.label}
              </span>

              <span className="font-semibold text-slate-950">
                {item.value}
              </span>
            </div>

            <div className="h-2 overflow-hidden rounded-full bg-slate-100">
              <div
                className={`h-full rounded-full ${item.className}`}
                style={{
                  width: `${item.percentage * 2}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}