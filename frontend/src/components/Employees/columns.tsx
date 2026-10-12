import type { ColumnDef } from "@tanstack/react-table"

import type { EmployeePublic } from "@/client"
import { EmployeeActionsMenu } from "./EmployeeActionsMenu"
import { MetaDataCell } from "../Common/columns"

export const getColumns = (
  isSuperuser: boolean,
): ColumnDef<EmployeePublic>[] => {
  const columns: ColumnDef<EmployeePublic>[] = [
    {
      accessorKey: "name",
      header: "Name",
      enableSorting: true,
      cell: ({ row }) => (
        <span className="font-medium">{row.original.name}</span>
      ),
    },
    {
      accessorKey: "position",
      header: "Position",
      enableSorting: true,
      cell: ({ row }) => (
        <span className="text-muted-foreground">{row.original.position}</span>
      ),
    },
  ]

  if (isSuperuser) {
    columns.push(
      {
        id: "metadata",
        header: "Metadata",
        enableSorting: false,
        cell: ({ row }) => <MetaDataCell metadata={row.original} />,
      },
      {
        id: "actions",
        header: () => <span className="sr-only">Actions</span>,
        enableSorting: false,
        cell: ({ row }) => (
          <div className="flex justify-end">
            <EmployeeActionsMenu employee={row.original} />
          </div>
        ),
      },
    )
  }

  return columns
}