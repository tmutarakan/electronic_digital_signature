import type { ColumnDef } from "@tanstack/react-table"

import type { EmployeePublic } from "@/client"
import { EmployeeActionsMenu } from "./EmployeeActionsMenu"
import { MetaDataCell } from "../Common/columns"

export const columns: ColumnDef<EmployeePublic>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => <span className="font-medium">{row.original.name}</span>,
  },
  {
    accessorKey: "position",
    header: "Position",
    cell: ({ row }) => (
      <span className="font-light">{row.original.position}</span>
    ),
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
        <EmployeeActionsMenu employee={row.original} />
      </div>
    ),
  },
]
