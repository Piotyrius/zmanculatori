import type { Metadata } from 'next';

export const dynamic = 'force-dynamic';

type ProjectDetailProps = {
  params: Promise<{ id: string }>;
};

export async function generateMetadata(
  props: ProjectDetailProps,
): Promise<Metadata> {
  const { id } = await props.params;
  return {
    title: `Project ${id}`,
  };
}

export default async function ProjectDetailPage(props: ProjectDetailProps) {
  const { id } = await props.params;

  return (
    <div className="space-y-4">
      <header>
        <h1 className="text-2xl font-semibold text-slate-50">
          Project #{id}
        </h1>
        <p className="mt-1 text-sm text-slate-400">
          Pattern versions and regeneration tools for this project.
        </p>
      </header>
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-sm text-slate-300">
        Project history and pattern list will be implemented here.
      </div>
    </div>
  );
}


