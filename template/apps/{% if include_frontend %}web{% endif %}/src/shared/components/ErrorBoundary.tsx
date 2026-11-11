import { Component, type ErrorInfo, type ReactNode } from "react";

interface State {
  error: Error | null;
}

export class ErrorBoundary extends Component<{ children: ReactNode }, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // Send to your error monitoring (e.g. Sentry) here.
    console.error(error, info.componentStack);
  }

  render() {
    if (this.state.error) {
      return (
        <div className="state state-error" role="alert">
          <p className="state-title">Something went wrong.</p>
          <button className="btn btn-secondary" onClick={() => window.location.reload()}>
            Reload
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
