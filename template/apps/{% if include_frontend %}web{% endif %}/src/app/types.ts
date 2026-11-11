import type { ReactElement } from "react";

/** Every feature exports `featureRoutes: FeatureRoute[]` from its routes.tsx. */
export interface FeatureRoute {
  /** Path relative to the app root, e.g. "items" or "items/:id". Omit for the index page. */
  path?: string;
  index?: boolean;
  element: ReactElement;
  /** Shown in the sidebar when present. Lower order = higher in the list. */
  nav?: { label: string; order: number };
}
