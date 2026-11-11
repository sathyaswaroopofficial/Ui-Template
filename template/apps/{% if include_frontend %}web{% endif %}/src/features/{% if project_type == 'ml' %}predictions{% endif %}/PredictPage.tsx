import { useState, type FormEvent } from "react";
import { Button } from "@/shared/components/Button";
import { ErrorState } from "@/shared/components/StateViews";
import { usePredict } from "./api";

const N_FEATURES = 4;

export function PredictPage() {
  const [values, setValues] = useState<string[]>(Array(N_FEATURES).fill("0"));
  const predict = usePredict();
  const data = predict.data;
  const result = data?.predictions[0];

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    predict.mutate([values.map(Number)]);
  }

  return (
    <section>
      <h1>Predict</h1>
      <form className="card" onSubmit={onSubmit}>
        {values.map((v, i) => (
          <div className="field" key={i}>
            <label htmlFor={`f${i}`}>Feature {i + 1}</label>
            <input
              id={`f${i}`}
              type="number"
              step="any"
              value={v}
              onChange={(e) => setValues(values.map((old, j) => (j === i ? e.target.value : old)))}
            />
          </div>
        ))}
        <Button type="submit" loading={predict.isPending}>
          Run prediction
        </Button>
      </form>

      {predict.isError && <ErrorState message={predict.error.message} />}
      {data && result && (
        <div className="card" aria-live="polite">
          <p>
            Predicted class <strong>{result.label}</strong> with{" "}
            <strong>{(result.confidence * 100).toFixed(1)}%</strong> confidence
          </p>
          {result.confidence < 0.6 && <p className="field-error">Low confidence: review this result.</p>}
          <p className="muted">Model version {data.model_version}</p>
        </div>
      )}
    </section>
  );
}
