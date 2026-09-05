import type { ColumnDef } from "@tanstack/react-table"
import { Check, Copy } from "lucide-react"

import type { OrganizationPublic } from "@/client"
import { Button } from "@/components/ui/button"
import { useCopyToClipboard } from "@/hooks/useCopyToClipboard"
import { OrganizationActionsMenu } from "./OrganizationActionsMenu"

function _CopyId({ id }: { id: string }) {
  const [copiedText, copy] = useCopyToClipboard()
  const isCopied = copiedText === id

  return (
    <div className="flex items-center gap-1.5 group">
      <span className="font-mono text-xs text-muted-foreground">{id}</span>
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
  )
}

export const columns: ColumnDef<OrganizationPublic>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => <span className="font-medium">{row.original.name}</span>,
  },
  {
    accessorKey: "owner",
    header: "OWNER",
    cell: ({ row }) => (
      <span className="font-light">{row.original.owner.email}</span>
    ),
  },
  {
    accessorKey: "created_at",
    header: "CREATED AT",
    cell: ({ row }) => (
      <span className="font-light">
        {new Date(row.original.created_at).toLocaleString()}
      </span>
    ),
  },
  {
    accessorKey: "updated_at",
    header: "UPDATED AT",
    cell: ({ row }) => (
      <span className="font-light">
        {new Date(row.original.updated_at).toLocaleString()}
      </span>
    ),
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <OrganizationActionsMenu organization={row.original} />
      </div>
    ),
  },
]
