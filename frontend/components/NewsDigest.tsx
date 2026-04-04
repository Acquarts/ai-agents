"use client";

import { useState } from "react";
import { ArticleCard } from "./ArticleCard";
import { CategoryFilter } from "./CategoryFilter";
import { Article, RunInfo } from "@/lib/db";

interface DigestData {
  date: string;
  articles: Article[];
  total: number;
  category_counts: { category: string; count: number }[];
  run_info: RunInfo | null;
}

export function NewsDigest({ initialData }: { initialData: DigestData }) {
  const [activeCategory, setActiveCategory] = useState("all");

  const filtered =
    activeCategory === "all"
      ? initialData.articles
      : initialData.articles.filter((a) => a.category === activeCategory);

  const highCount = initialData.articles.filter((a) => a.importance === "high").length;

  return (
    <div className="flex flex-col gap-6">
      {/* Run info banner */}
      {initialData.run_info && (
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <span
            className={`w-2 h-2 rounded-full ${
              initialData.run_info.status === "success" ? "bg-green-400" : "bg-red-400"
            }`}
          />
          Ultima actualización:{" "}
          {initialData.run_info.finished_at
            ? new Date(initialData.run_info.finished_at).toLocaleString("es-ES")
            : "en progreso"}{" "}
          · {initialData.run_info.articles_fetched} articulos recuperados ·{" "}
          {initialData.run_info.articles_summarized} resumidos
        </div>
      )}

      {/* Stats */}
      <div className="flex gap-4">
        <div className="bg-gray-900 text-white rounded-xl px-5 py-4 flex flex-col gap-0.5">
          <span className="text-3xl font-bold">{initialData.total}</span>
          <span className="text-xs text-gray-400">noticias hoy</span>
        </div>
        {highCount > 0 && (
          <div className="bg-red-50 border border-red-200 rounded-xl px-5 py-4 flex flex-col gap-0.5">
            <span className="text-3xl font-bold text-red-600">{highCount}</span>
            <span className="text-xs text-red-400">alta importancia</span>
          </div>
        )}
      </div>

      {/* Category filter */}
      <CategoryFilter
        active={activeCategory}
        counts={initialData.category_counts}
        onChange={setActiveCategory}
      />

      {/* Articles grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-16 text-gray-400">
          <p className="text-4xl mb-3">📭</p>
          <p>No hay articulos para esta categoria hoy.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map((article) => (
            <ArticleCard key={article.id} article={article} />
          ))}
        </div>
      )}
    </div>
  );
}
