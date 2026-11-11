import { useMutation } from "@tanstack/react-query";
import { api } from "@/shared/api/apiClient";

export interface PredictResponse {
  model_version: string;
  predictions: { label: number; confidence: number }[];
}

export function usePredict() {
  return useMutation({
    mutationFn: (rows: number[][]) => api.post<PredictResponse>("/api/v1/predictions", { rows }),
  });
}
