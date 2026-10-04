import { Download, EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { ElectronicDigitalSignaturePublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu"
import DeleteElectronicDigitalSignature from "./DeleteElectronicDigitalSignature"
import EditElectronicDigitalSignature from "./EditElectronicDigitalSignature"

interface ElectronicDigitalSignatureActionsMenuProps {
  signature: ElectronicDigitalSignaturePublic
}

export const ElectronicDigitalSignatureActionsMenu = ({
  signature,
}: ElectronicDigitalSignatureActionsMenuProps) => {
  const [menuOpen, setMenuOpen] = useState(false)
  const [editOpen, setEditOpen] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)

  return (
    <>
      <DropdownMenu open={menuOpen} onOpenChange={setMenuOpen}>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="icon" aria-label="Действия">
            <EllipsisVertical />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem asChild>
            <a
              href={signature.certificate_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2"
            >
              <Download className="size-4" />
              Download Certificate
            </a>
          </DropdownMenuItem>
          <DropdownMenuItem asChild>
            <a
              href={signature.container_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2"
            >
              <Download className="size-4" />
              Download Container
            </a>
          </DropdownMenuItem>

          <DropdownMenuSeparator />

          <DropdownMenuItem
            onSelect={(e) => {
              // preventDefault — чтобы Radix не «съел» открытие диалога
              e.preventDefault()
              setMenuOpen(false)
              setEditOpen(true)
            }}
          >
            Edit ElectronicDigitalSignature
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem
            onSelect={(e) => {
              e.preventDefault()
              setMenuOpen(false)
              setDeleteOpen(true)
            }}
            className="text-destructive focus:text-destructive"
          >
            Delete ElectronicDigitalSignature
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Диалоги рендерятся ВНЕ DropdownMenu — это ключевой момент */}
      <EditElectronicDigitalSignature
        electronicDigitalSignature={signature}
        open={editOpen}
        onOpenChange={setEditOpen}
        onSuccess={() => setEditOpen(false)}
      />

      <DeleteElectronicDigitalSignature
        id={signature.id}
        open={deleteOpen}
        onOpenChange={setDeleteOpen}
        onSuccess={() => setDeleteOpen(false)}
      />
    </>
  )
}
