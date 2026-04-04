import { Article } from "@/lib/db";

const IMPORTANCE_STYLES: Record<string, string> = {
  high: "bg-red-100 text-red-700 border-red-200",
  medium: "bg-amber-100 text-amber-700 border-amber-200",
  low: "bg-gray-100 text-gray-600 border-gray-200",
};

const CATEGORY_STYLES: Record<string, string> = {
  Research: "bg-blue-100 text-blue-700",
  Products: "bg-purple-100 text-purple-700",
  Industry: "bg-green-100 text-green-700",
  Tooling: "bg-orange-100 text-orange-700",
};

function formatDate(iso: string | null): string {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleDateString("es-ES", {
      day: "numeric",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return "";
  }
}

export function ArticleCard({ article }: { article: Article }) {
  const importance = article.importance ?? "medium";
  const category = article.category ?? "Industry";

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow flex flex-col gap-3">
      <div className="flex items-start justify-between gap-3">
        <div className="flex gap-2 flex-wrap">
          <span
            className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${IMPORTANCE_STYLES[importance] ?? IMPORTANCE_STYLES.medium}`}
          >
            {importance === "high" ? "★ " : ""}
            {importance.charAt(0).toUpperCase() + importance.slice(1)}
          </span>
          <span
            className={`text-xs font-medium px-2 py-0.5 rounded-full ${CATEGORY_STYLES[category] ?? "bg-gray-100 text-gray-600"}`}
          >
            {category}
          </span>
        </div>
        <span className="text-xs text-gray-400 shrink-0">
          {article.source_name}
        </span>
      </div>

      <a
        href={article.original_url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-gray-900 font-semibold text-sm leading-snug hover:text-blue-600 transition-colors"
      >
        {article.title}
      </a>

      {article.summary && (
        <p className="text-gray-600 text-sm leading-relaxed">{article.summary}</p>
      )}

      <div className="flex items-center justify-between mt-auto pt-2 border-t border-gray-100">
        <span className="text-xs text-gray-400">
          {formatDate(article.published_at ?? article.fetched_at)}
        </span>
        <a
          href={article.original_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-blue-500 hover:text-blue-700 font-medium"
        >
          Leer mas →
        </a>
      </div>
    </div>
  );
}
