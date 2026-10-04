import type { ColumnDef } from "@tanstack/react-table"

import type { ElectronicDigitalSignaturePublic } from "@/client"
import { ElectronicDigitalSignatureActionsMenu } from "./ElectronicDigitalSignatureActionsMenu"

/*function _CopyId({ id }: { id: string }) {
  const [copiedText, copy] = useCopyToClipboard()
  const isCopied = copiedText === id

  return (
    <div className="flex items-center gap-1.5 group">
      <span className="font-mono text-xs text-muted-foreground">{id}</span>
      <Button
        variant="ghost"
        size="icon"
        className="size-6 opacity-0 group-hover:opacity-100 transition-opacity"
        onClick={() => copy(id)}
      >
        {isCopied ? (
          <Check className="size-3 text-green-500" />
        ) : (
          <Copy className="size-3" />
        )}
        <span className="sr-only">Copy ID</span>
      </Button>
    </div>
  )
}*/

export const columns: ColumnDef<ElectronicDigitalSignaturePublic>[] = [
  {
    accessorKey: "date_certificate",
    header: "Date Certificate",
    cell: ({ row }) => (
      <span className="font-medium">
        {new Date(row.original.date_certificate).toLocaleString()}
      </span>
    ),
  },
  {
    accessorKey: "file_certificate",
    header: "File Certificate",
    cell: ({ row }) => (
      <a
        href={row.original.certificate_url}
        target="_blank"
        rel="noopener noreferrer"
        className="font-medium text-primary underline underline-offset-2 hover:opacity-80"
      >
        Download Certificate
      </a>
    ),
  },
  {
    accessorKey: "date_container",
    header: "Date Container",
    cell: ({ row }) => (
      <span className="font-medium">
        {new Date(row.original.date_container).toLocaleString()}
      </span>
    ),
  },
  {
    accessorKey: "file_container",
    header: "File Container",
    cell: ({ row }) => (
      <a
        href={row.original.container_url}
        target="_blank"
        rel="noopener noreferrer"
        className="font-medium text-primary underline underline-offset-2 hover:opacity-80"
      >
        Download Container
      </a>
    ),
  },
  {
    accessorKey: "owner",
    header: "OWNER",
    cell: ({ row }) => (
      <span className="font-light">{row.original.owner.email}</span>
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
    accessorKey: "created_at",
    header: "CREATED AT",
    cell: ({ row }) => (
      <span className="font-light">
        {new Date(row.original.created_at).toLocaleString()}
      </span>
    ),
  },
  {
    accessorKey: "updated_at",
    header: "UPDATED AT",
    cell: ({ row }) => (
      <span className="font-light">
        {new Date(row.original.updated_at).toLocaleString()}
      </span>
    ),
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
