"use client";

const CATEGORIES = ["all", "Research", "Products", "Industry", "Tooling"];

const CATEGORY_ICONS: Record<string, string> = {
  all: "✦",
  Research: "🔬",
  Products: "🚀",
  Industry: "🏢",
  Tooling: "🛠️",
};

interface CategoryFilterProps {
  active: string;
  counts: { category: string; count: number }[];
  onChange: (category: string) => void;
}

export function CategoryFilter({ active, counts, onChange }: CategoryFilterProps) {
  const countMap = Object.fromEntries(counts.map((c) => [c.category, c.count]));
  const total = counts.reduce((sum, c) => sum + c.count, 0);

  return (
    <div className="flex gap-2 flex-wrap">
      {CATEGORIES.map((cat) => {
        const count = cat === "all" ? total : (countMap[cat] ?? 0);
        const isActive = active === cat;
        return (
          <button
            key={cat}
            onClick={() => onChange(cat)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium transition-colors border ${
              isActive
                ? "bg-gray-900 text-white border-gray-900"
                : "bg-white text-gray-600 border-gray-200 hover:border-gray-400"
            }`}
          >
            <span>{CATEGORY_ICONS[cat]}</span>
            <span>{cat === "all" ? "Todas" : cat}</span>
            <span
              className={`text-xs px-1.5 py-0.5 rounded-full ${
                isActive ? "bg-white/20 text-white" : "bg-gray-100 text-gray-500"
              }`}
            >
              {count}
            </span>
          </button>
        );
      })}
    </div>
  );
}
