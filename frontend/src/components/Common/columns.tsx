import { Check, Copy } from "lucide-react";

import { useCopyToClipboard } from "@/hooks/useCopyToClipboard";
import { Button } from "@/components/ui/button";

function CopyId({ id }: { id: string }) {
  const [copiedText, copy] = useCopyToClipboard();
  const isCopied = copiedText === id;

  return (
    <div className="flex items-center gap-1.5 group">
      <span className="font-mono text-xs text-muted-foreground">ID: {id}</span>
      <Button
        variant="ghost"
        size="icon"
        className="size-6 opacity-0 group-hover:opacity-100 transition-opacity"
        onClick={() => copy(id)}
      >
        {isCopied ? (
          <Check className="size-3 text-green-500" />
        ) : (
          <Copy className="size-3" />
        )}
        <span className="sr-only">Copy ID</span>
      </Button>
    </div>
  );
}

const dateFormatter = new Intl.DateTimeFormat("ru-RU", {
  dateStyle: "short",
  timeStyle: "short",
});

const formatDate = (value: string | null | undefined) => {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";
  return dateFormatter.format(date);
};

interface Details {
  id: string;
  owner?: { email: string } | null;
  created_at: string | null | undefined;
  updated_at: string | null | undefined;
}

interface DetailsCellProps {
  details: Details;
}

export const DetailsCell = ({ details }: DetailsCellProps) => {
  const { id, owner, created_at, updated_at } = details;

  return (
    <div className="flex flex-col gap-0.5 text-sm font-light">
      <CopyId id={id} />
      <span>
        <span className="text-muted-foreground">Owner: </span>
        {owner?.email ?? "—"}
      </span>
      <span>
        <span className="text-muted-foreground">Created: </span>
        {formatDate(created_at)}
      </span>
      <span>
        <span className="text-muted-foreground">Updated: </span>
        {formatDate(updated_at)}
      </span>
    </div>
  );
};
