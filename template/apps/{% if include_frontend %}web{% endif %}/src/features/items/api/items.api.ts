import { api } from "@/shared/api/apiClient";
import type { Item, ItemCreate } from "../types";

const BASE = "/api/v1/items";

export const itemsApi = {
  list: () => api.get<Item[]>(BASE),
  create: (data: ItemCreate) => api.post<Item>(BASE, data),
  remove: (id: number) => api.delete(`${BASE}/${id}`),
};
