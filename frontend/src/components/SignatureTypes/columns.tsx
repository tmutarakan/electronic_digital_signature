import type { ColumnDef } from "@tanstack/react-table";

import type { SignatureTypePublic } from "@/client";
import { SignatureTypeActionsMenu } from "./SignatureTypeActionsMenu";
import { MetaDataCell } from "../Common/columns";

export const getColumns = (
  isSuperuser: boolean,
): ColumnDef<SignatureTypePublic>[] => {
  const columns: ColumnDef<SignatureTypePublic>[] = [
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
            <SignatureTypeActionsMenu signatureType={row.original} />
          </div>
        ),
      },
    );
  }

  return columns;
};
