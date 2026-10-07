import type { ColumnDef } from "@tanstack/react-table"

import type { SignatureTypePublic } from "@/client"
import { SignatureTypeActionsMenu } from "./SignatureTypeActionsMenu"
import { MetaDataCell } from "../Common/columns"

export const columns: ColumnDef<SignatureTypePublic>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => <span className="font-medium">{row.original.name}</span>,
  },
  {
    id: "metadata",
    header: "metadata",
    enableSorting: false,
    cell: ({ row }) => <MetaDataCell metadata={row.original} />,
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <SignatureTypeActionsMenu signatureType={row.original} />
      </div>
    ),
  },
]
