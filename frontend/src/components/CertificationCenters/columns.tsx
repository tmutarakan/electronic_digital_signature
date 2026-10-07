import type { ColumnDef } from "@tanstack/react-table"

import type { CertificationCenterPublic } from "@/client"
import { CertificationCenterActionsMenu } from "./CertificationCenterActionsMenu"
import { MetaDataCell } from "../Common/columns"

export const columns: ColumnDef<CertificationCenterPublic>[] = [
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
        <CertificationCenterActionsMenu certificationCenter={row.original} />
      </div>
    ),
  },
]
