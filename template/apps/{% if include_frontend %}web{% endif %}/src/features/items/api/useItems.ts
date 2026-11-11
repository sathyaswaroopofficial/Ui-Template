import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { ItemCreate } from "../types";
import { itemsApi } from "./items.api";

export const itemKeys = {
  all: ["items"] as const,
};

export function useItems() {
  return useQuery({ queryKey: itemKeys.all, queryFn: itemsApi.list });
}

export function useCreateItem() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: ItemCreate) => itemsApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: itemKeys.all }),
  });
}

export function useDeleteItem() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => itemsApi.remove(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: itemKeys.all }),
  });
}
