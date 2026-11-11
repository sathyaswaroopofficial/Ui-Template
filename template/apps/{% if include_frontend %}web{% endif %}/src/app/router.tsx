import { createBrowserRouter, type RouteObject } from "react-router-dom";
import { NotFoundPage } from "@/shared/components/NotFoundPage";
import { AppShell } from "./layout/AppShell";
import { featureRoutes } from "./routes";

const children: RouteObject[] = featureRoutes.map((r) =>
  r.index ? { index: true, element: r.element } : { path: r.path, element: r.element },
);

export const router = createBrowserRouter(
  [
    {
      path: "/",
      element: <AppShell />,
      children: [...children, { path: "*", element: <NotFoundPage /> }],
    },
  ],
  { future: { v7_relativeSplatPath: true } },
);
