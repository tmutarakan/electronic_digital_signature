import type { ColumnDef } from "@tanstack/react-table";

import type { OrganizationPublic } from "@/client";
import { OrganizationActionsMenu } from "./OrganizationActionsMenu";
import { MetaDataCell } from "../Common/columns";

export const getColumns = (
  isSuperuser: boolean,
): ColumnDef<OrganizationPublic>[] => {
  const columns: ColumnDef<OrganizationPublic>[] = [
    {
      accessorKey: "name",
      header: "Name",
      enableSorting: true,
      cell: ({ row }) => (
        <span className="font-medium">{row.original.name}</span>
      ),
    },
  ];

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
        enableHiding: false,
        cell: ({ row }) => (
          <div className="flex justify-end">
            <OrganizationActionsMenu organization={row.original} />
          </div>
        ),
      },
    );
  }

  return columns;
};
