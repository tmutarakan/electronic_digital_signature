import type { ColumnDef } from "@tanstack/react-table"

import type { ElectronicDigitalSignaturePublic } from "@/client"
import { ElectronicDigitalSignatureActionsMenu } from "./ElectronicDigitalSignatureActionsMenu"
import { DetailsCell } from "../Common/columns"

export const columns: ColumnDef<ElectronicDigitalSignaturePublic>[] = [
  {
    accessorKey: "date_certificate",
    header: "Date Certificate",
    cell: ({ row }) => (
      <span className="font-medium whitespace-normal">
        {new Date(row.original.date_certificate).toLocaleString()}
      </span>
    ),
  },
  {
    accessorKey: "date_container",
    header: "Date Container",
    cell: ({ row }) => (
      <span className="font-medium whitespace-normal">
        {new Date(row.original.date_container).toLocaleString()}
      </span>
    ),
  },
  {
    accessorKey: "organization",
    header: "Organization",
    cell: ({ row }) => (
      <span className="font-light">{row.original.organization.name}</span>
    ),
  },
  {
    accessorKey: "signature_type",
    header: "Signature Type",
    cell: ({ row }) => (
      <span className="font-light">{row.original.signature_type.name}</span>
    ),
  },
  {
    accessorKey: "employee",
    header: "Employee",
    cell: ({ row }) => (
      <span className="font-light">{row.original.employee.name}</span>
    ),
  },
  {
    accessorKey: "certification_center",
    header: "Certification Center",
    cell: ({ row }) => (
      <span className="font-light">
        {row.original.certification_center.name}
      </span>
    ),
  },
  {
    id: "details",
    header: "details",
    enableSorting: false,
    cell: ({ row }) => <DetailsCell details={row.original} />,
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <ElectronicDigitalSignatureActionsMenu signature={row.original} />
      </div>
    ),
  },
]
