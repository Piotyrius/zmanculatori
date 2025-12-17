import type { Metadata } from 'next';

export const dynamic = 'force-dynamic';

type ProductPageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata(
  props: ProductPageProps,
): Promise<Metadata> {
  const { slug } = await props.params;
  return {
    title: `Configure ${slug} pattern`,
  };
}

export default async function ProductPage(props: ProductPageProps) {
  const { slug } = await props.params;

  return (
    <div className="space-y-4">
      <header>
        <h1 className="text-2xl font-semibold text-slate-50 capitalize">
          {slug} pattern
        </h1>
        <p className="mt-1 text-sm text-slate-400">
          Step-by-step configuration wizard for this garment.
        </p>
      </header>
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-sm text-slate-300">
        Product configuration wizard will be implemented here.
      </div>
    </div>
  );
}


