// Tip: after `npm run gen:api`, replace these with the generated types:
//   import type { components } from "@/shared/api/generated/schema";
//   export type Item = components["schemas"]["ItemRead"];
export interface Item {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
}

export interface ItemCreate {
  name: string;
  description?: string | null;
}
