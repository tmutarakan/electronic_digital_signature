import type { ColumnDef } from "@tanstack/react-table";

import type { CertificationCenterPublic } from "@/client";
import { CertificationCenterActionsMenu } from "./CertificationCenterActionsMenu";
import { MetaDataCell } from "../Common/columns";

export const getColumns = (
  isSuperuser: boolean,
): ColumnDef<CertificationCenterPublic>[] => {
  const columns: ColumnDef<CertificationCenterPublic>[] = [
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
        cell: ({ row }) => (
          <div className="flex justify-end">
            <CertificationCenterActionsMenu
              certificationCenter={row.original}
            />
          </div>
        ),
      },
    );
  }

  return columns;
};
