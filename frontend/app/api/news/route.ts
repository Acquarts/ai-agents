import { NextRequest, NextResponse } from "next/server";
import { getDb, Article, RunInfo } from "@/lib/db";
import { existsSync } from "fs";
import path from "path";

const DB_PATH = path.join(process.cwd(), "..", "db", "news.db");

export async function GET(request: NextRequest) {
  if (!existsSync(DB_PATH)) {
    return NextResponse.json(
      { error: "Database not found. Run the Python pipeline first." },
      { status: 503 }
    );
  }

  try {
    const db = getDb();
    const { searchParams } = new URL(request.url);

    const date = searchParams.get("date") ?? new Date().toISOString().slice(0, 10);
    const category = searchParams.get("category");

    let query = `
      SELECT * FROM articles
      WHERE DATE(published_at) = ? AND summary IS NOT NULL
    `;
    const params: (string | number)[] = [date];

    if (category && category !== "all") {
      query += " AND category = ?";
      params.push(category);
    }

    query += `
      ORDER BY
        CASE importance WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
        published_at DESC
    `;

    const articles = db.prepare(query).all(...params) as Article[];

    const run = db
      .prepare("SELECT * FROM runs ORDER BY id DESC LIMIT 1")
      .get() as RunInfo | undefined;

    const categoryCounts = db
      .prepare(
        `SELECT category, COUNT(*) as count FROM articles
         WHERE DATE(published_at) = ? AND summary IS NOT NULL AND category IS NOT NULL
         GROUP BY category ORDER BY count DESC`
      )
      .all(date) as { category: string; count: number }[];

    return NextResponse.json({
      date,
      articles,
      total: articles.length,
      category_counts: categoryCounts,
      run_info: run ?? null,
    });
  } catch (error) {
    console.error("[api/news] Error:", error);
    return NextResponse.json(
      { error: "Failed to query database" },
      { status: 500 }
    );
  }
}
