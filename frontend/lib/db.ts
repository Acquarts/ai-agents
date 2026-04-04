import Database from "better-sqlite3";
import path from "path";

const DB_PATH = path.join(process.cwd(), "..", "db", "news.db");

let db: Database.Database | null = null;

export function getDb(): Database.Database {
  if (!db) {
    db = new Database(DB_PATH, { readonly: true });
  }
  return db;
}

export interface Article {
  id: number;
  source_name: string;
  source_url: string;
  title: string;
  original_url: string;
  published_at: string | null;
  fetched_at: string;
  summary: string | null;
  category: string | null;
  importance: string | null;
  raw_content: string | null;
}

export interface RunInfo {
  id: number;
  started_at: string;
  finished_at: string | null;
  articles_fetched: number;
  articles_summarized: number;
  status: string | null;
  error_message: string | null;
}
