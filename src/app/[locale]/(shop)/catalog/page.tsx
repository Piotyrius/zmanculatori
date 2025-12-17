export const dynamic = 'force-dynamic';

export default function CatalogPage() {
  return (
    <div className="space-y-4">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-50">
            Garment catalog
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Browse base blocks and pattern types like a clothing shop.
          </p>
        </div>
      </header>
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-sm text-slate-300">
        Catalog UI will appear here (filters, categories, product cards).
      </div>
    </div>
  );
}


