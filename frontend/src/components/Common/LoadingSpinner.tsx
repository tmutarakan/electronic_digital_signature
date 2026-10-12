// components/Common/LoadingSpinner.tsx
import { Loader2 } from "lucide-react";

interface LoadingSpinnerProps {
  label?: string;
  className?: string;
}

export function LoadingSpinner({
  label = "Loading...",
  className,
}: LoadingSpinnerProps) {
  return (
    <div
      className={`flex items-center justify-center py-12 ${className ?? ""}`}
      role="status"
      aria-live="polite"
    >
      <Loader2 className="size-6 animate-spin text-muted-foreground" />
      <span className="sr-only">{label}</span>
    </div>
  );
}
