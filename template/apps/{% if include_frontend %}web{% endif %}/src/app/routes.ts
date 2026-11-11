import type { FeatureRoute } from "./types";

// Auto-collect routes from every feature: adding a feature never requires editing this file.
const modules = import.meta.glob<{ featureRoutes: FeatureRoute[] }>("../features/*/routes.tsx", {
  eager: true,
});

export const featureRoutes: FeatureRoute[] = Object.values(modules).flatMap((m) => m.featureRoutes);

export const navItems = featureRoutes
  .filter((r) => r.nav)
  .sort((a, b) => a.nav!.order - b.nav!.order)
  .map((r) => ({ to: r.index ? "/" : `/${r.path}`, label: r.nav!.label }));
