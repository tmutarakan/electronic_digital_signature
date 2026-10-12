import type { ColumnDef } from "@tanstack/react-table";

import type { ElectronicDigitalSignaturePublic } from "@/client";
import { ElectronicDigitalSignatureActionsMenu } from "./ElectronicDigitalSignatureActionsMenu";
import { MetaDataCell } from "../Common/columns";

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

export const getColumns = (
  isSuperuser: boolean,
): ColumnDef<ElectronicDigitalSignaturePublic>[] => {
  const columns: ColumnDef<ElectronicDigitalSignaturePublic>[] = [
    {
      accessorKey: "date_certificate",
      header: "Date Certificate",
      enableSorting: true,
      cell: ({ row }) => (
        <span className="font-medium whitespace-nowrap">
          {formatDate(row.original.date_certificate)}
        </span>
      ),
    },
    {
      accessorKey: "date_container",
      header: "Date Container",
      enableSorting: true,
      cell: ({ row }) => (
        <span className="font-medium whitespace-nowrap">
          {formatDate(row.original.date_container)}
        </span>
      ),
    },
    {
      accessorKey: "organization.name",
      header: "Organization",
      enableSorting: true,
      cell: ({ row }) => (
        <span className="font-light">
          {row.original.organization?.name ?? "—"}
        </span>
      ),
    },
    {
      accessorKey: "signature_type.name",
      header: "Signature Type",
      enableSorting: true,
      cell: ({ row }) => (
        <span className="font-light">
          {row.original.signature_type?.name ?? "—"}
        </span>
      ),
    },
    {
      accessorKey: "employee.name",
      header: "Employee",
      enableSorting: true,
      cell: ({ row }) => (
        <span className="font-light">{row.original.employee?.name ?? "—"}</span>
      ),
    },
    {
      accessorKey: "certification_center.name",
      header: "Certification Center",
      enableSorting: true,
      cell: ({ row }) => (
        <span className="font-light">
          {row.original.certification_center?.name ?? "—"}
        </span>
      ),
    },
  ];

  if (isSuperuser) {
      columns.push({
        id: "metadata",
        header: "Metadata",
        enableSorting: false,
        cell: ({ row }) => <MetaDataCell metadata={row.original} />,
      })
    }
  
    // actions — всем, но внутри Edit/Delete только для суперпользователя
    columns.push({
      id: "actions",
      header: () => <span className="sr-only">Actions</span>,
      enableSorting: false,
      enableHiding: false,
      cell: ({ row }) => (
        <div className="flex justify-end">
          <ElectronicDigitalSignatureActionsMenu
            signature={row.original}
            isSuperuser={isSuperuser}
          />
        </div>
      ),
    })

  return columns;
};
