import type { FeatureRoute } from "@/app/types";
import { PredictPage } from "./PredictPage";

export const featureRoutes: FeatureRoute[] = [
  { path: "predict", element: <PredictPage />, nav: { label: "Predict", order: 20 } },
];
