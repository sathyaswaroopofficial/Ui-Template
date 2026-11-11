import type { FeatureRoute } from "@/app/types";
import { ItemsPage } from "./pages/ItemsPage";

export const featureRoutes: FeatureRoute[] = [
  { path: "items", element: <ItemsPage />, nav: { label: "Items", order: 10 } },
];
