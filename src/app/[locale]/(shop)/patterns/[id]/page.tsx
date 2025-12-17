import type { Metadata } from 'next';

export const dynamic = 'force-dynamic';

type PatternPageProps = {
  params: Promise<{ id: string }>;
};

export async function generateMetadata(
  props: PatternPageProps,
): Promise<Metadata> {
  const { id } = await props.params;
  return {
    title: `Pattern ${id}`,
  };
}

export default async function PatternPage(props: PatternPageProps) {
  const { id } = await props.params;

  return (
    <div className="space-y-4">
      <header>
        <h1 className="text-2xl font-semibold text-slate-50">
          Pattern #{id}
        </h1>
        <p className="mt-1 text-sm text-slate-400">
          View the generated draft, inspect metadata, and export files.
        </p>
      </header>
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-sm text-slate-300">
        Pattern visualization and export tools will be implemented here.
      </div>
    </div>
  );
}


