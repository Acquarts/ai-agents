import { NewsDigest } from "@/components/NewsDigest";

async function getNewsData(date: string) {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "http://localhost:3000";
    const res = await fetch(`${baseUrl}/api/news?date=${date}`, {
      cache: "no-store",
    });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export default async function Home({
  searchParams,
}: {
  searchParams: Promise<{ date?: string }>;
}) {
  const params = await searchParams;
  const today = new Date().toISOString().slice(0, 10);
  const date = params.date ?? today;

  const data = await getNewsData(date);

  const formattedDate = new Date(date + "T12:00:00").toLocaleDateString("es-ES", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-3xl">🤖</span>
            <h1 className="text-2xl font-bold text-gray-900">AI News Daily</h1>
          </div>
          <p className="text-gray-500 text-sm ml-14 capitalize">{formattedDate}</p>

          {/* Date navigation */}
          <div className="flex gap-2 mt-4 ml-14">
            {[-2, -1, 0].map((offset) => {
              const d = new Date();
              d.setDate(d.getDate() + offset);
              const dStr = d.toISOString().slice(0, 10);
              const label =
                offset === 0
                  ? "Hoy"
                  : offset === -1
                  ? "Ayer"
                  : d.toLocaleDateString("es-ES", { weekday: "short", day: "numeric" });
              const isActive = dStr === date;
              return (
                <a
                  key={dStr}
                  href={`?date=${dStr}`}
                  className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-gray-900 text-white"
                      : "bg-white text-gray-600 border border-gray-200 hover:border-gray-400"
                  }`}
                >
                  {label}
                </a>
              );
            })}
          </div>
        </header>

        {/* Content */}
        {!data || data.error ? (
          <div className="text-center py-20">
            <p className="text-5xl mb-4">⚙️</p>
            <h2 className="text-xl font-semibold text-gray-700 mb-2">
              {data?.error ?? "No hay datos disponibles"}
            </h2>
            <p className="text-gray-500 text-sm max-w-md mx-auto mb-3">
              Ejecuta el pipeline de agentes primero:
            </p>
            <pre className="bg-gray-900 text-green-400 text-xs rounded-lg px-4 py-3 inline-block text-left">
              python agents/run_pipeline.py
            </pre>
          </div>
        ) : data.total === 0 ? (
          <div className="text-center py-20">
            <p className="text-5xl mb-4">📰</p>
            <h2 className="text-xl font-semibold text-gray-700 mb-2">
              Sin noticias para {formattedDate}
            </h2>
            <p className="text-gray-500 text-sm">
              El pipeline se ejecuta diariamente a las 7:00 AM.
            </p>
          </div>
        ) : (
          <NewsDigest initialData={data} />
        )}
      </div>
    </main>
  );
}
