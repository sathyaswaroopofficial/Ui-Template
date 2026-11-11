import { screen } from "@testing-library/react";
import { mockFetchOnce, renderWithProviders } from "@/test/utils";
import { ItemsPage } from "./ItemsPage";

describe("ItemsPage", () => {
  it("shows items from the API", async () => {
    mockFetchOnce([{ id: 1, name: "First item", description: null, created_at: "2026-01-01T00:00:00Z" }]);
    renderWithProviders(<ItemsPage />);
    expect(await screen.findByText("First item")).toBeInTheDocument();
  });

  it("shows the empty state", async () => {
    mockFetchOnce([]);
    renderWithProviders(<ItemsPage />);
    expect(await screen.findByText(/no items yet/i)).toBeInTheDocument();
  });

  it("shows the backend error message", async () => {
    mockFetchOnce({ error: { code: "internal_error", message: "Something went wrong" } }, 500);
    renderWithProviders(<ItemsPage />);
    expect(await screen.findByRole("alert")).toHaveTextContent("Something went wrong");
  });
});
