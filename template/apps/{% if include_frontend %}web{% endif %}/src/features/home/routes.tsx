import type { FeatureRoute } from "@/app/types";
import { HomePage } from "./HomePage";

export const featureRoutes: FeatureRoute[] = [
  { index: true, element: <HomePage />, nav: { label: "Home", order: 0 } },
];
