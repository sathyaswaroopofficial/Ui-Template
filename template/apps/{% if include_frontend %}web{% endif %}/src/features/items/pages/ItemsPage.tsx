import { useState, type FormEvent } from "react";
import { Button } from "@/shared/components/Button";
import { EmptyState, ErrorState, LoadingState } from "@/shared/components/StateViews";
import { useCreateItem, useDeleteItem, useItems } from "../api/useItems";

export function ItemsPage() {
  const items = useItems();
  const createItem = useCreateItem();
  const deleteItem = useDeleteItem();
  const [name, setName] = useState("");

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!name.trim()) return;
    createItem.mutate({ name }, { onSuccess: () => setName("") });
  }

  return (
    <section>
      <h1>Items</h1>

      <form className="card" onSubmit={onSubmit} noValidate>
        <div className="field">
          <label htmlFor="item-name">Name</label>
          <input
            id="item-name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            maxLength={120}
            aria-invalid={createItem.isError || undefined}
          />
          {createItem.isError && <span className="field-error">{createItem.error.message}</span>}
        </div>
        <Button type="submit" loading={createItem.isPending} disabled={!name.trim()}>
          Add item
        </Button>
      </form>

      <div className="card">
        {items.isPending ? (
          <LoadingState />
        ) : items.isError ? (
          <ErrorState message={items.error.message} onRetry={() => items.refetch()} />
        ) : items.data.length === 0 ? (
          <EmptyState title="No items yet. Add your first one above." />
        ) : (
          <ul className="list">
            {items.data.map((item) => (
              <li key={item.id} className="list-row">
                <span>{item.name}</span>
                <Button
                  variant="danger"
                  onClick={() => deleteItem.mutate(item.id)}
                  loading={deleteItem.isPending && deleteItem.variables === item.id}
                  aria-label={`Delete ${item.name}`}
                >
                  Delete
                </Button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
