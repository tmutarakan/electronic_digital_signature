import type { ColumnDef } from "@tanstack/react-table";

import type { OrganizationPublic } from "@/client";
import { OrganizationActionsMenu } from "./OrganizationActionsMenu";
import { DetailsCell } from "../Common/columns"

export const columns: ColumnDef<OrganizationPublic>[] = [
  {
    accessorKey: "name",
    header: "name",
    cell: ({ row }) => <span className="font-medium">{row.original.name}</span>,
  },
  {
    id: "details",
    header: "details",
    enableSorting: false,
    cell: ({ row }) => <DetailsCell details={row.original} />,
  },
  {
    id: "actions",
    enableSorting: false,
    enableHiding: false,
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <OrganizationActionsMenu organization={row.original} />
      </div>
    ),
  },
];
