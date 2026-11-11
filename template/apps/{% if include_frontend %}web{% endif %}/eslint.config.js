import js from "@eslint/js";
import reactHooks from "eslint-plugin-react-hooks";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["dist", "src/shared/api/generated"] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ["**/*.{ts,tsx}"],
    languageOptions: { ecmaVersion: 2022, globals: globals.browser },
    plugins: { "react-hooks": reactHooks },
    rules: {
      ...reactHooks.configs.recommended.rules,
      // Features must not reach into each other's internals; import from a feature's index.ts.
      "no-restricted-imports": [
        "error",
        { patterns: [{ group: ["@/features/*/*"], message: "Import from the feature's index.ts instead." }] },
      ],
    },
  },
);
