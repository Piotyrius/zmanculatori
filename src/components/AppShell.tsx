'use client';

import { ReactNode } from 'react';
import Link from 'next/link';
import { useLocale } from 'next-intl';
import { usePathname } from 'next/navigation';

type NavItem = {
  href: (locale: string) => string;
  label: string;
};

const navItems: NavItem[] = [
  { href: (locale) => `/${locale}/catalog`, label: 'Catalog' },
  { href: (locale) => `/${locale}/projects`, label: 'Projects' },
  { href: (locale) => `/${locale}/measurements`, label: 'Measurements' },
  { href: (locale) => `/${locale}/profiles`, label: 'Profiles' },
  { href: (locale) => `/${locale}/account`, label: 'Account' },
];

export default function AppShell({ children }: { children: ReactNode }) {
  const locale = useLocale();
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6 lg:py-8">
        <aside className="hidden w-56 shrink-0 rounded-2xl border border-slate-800 bg-slate-900/60 p-4 lg:block">
          <nav className="space-y-1 text-sm">
            {navItems.map((item) => {
              const href = item.href(locale);
              const active =
                pathname === href || pathname.startsWith(`${href}/`);
              return (
                <Link
                  key={item.label}
                  href={href}
                  className={`block rounded-md px-3 py-2 transition ${
                    active
                      ? 'bg-sky-500/10 text-sky-300'
                      : 'text-slate-300 hover:bg-slate-800 hover:text-slate-50'
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </aside>
        <main className="flex-1 pb-12">{children}</main>
      </div>
    </div>
  );
}


