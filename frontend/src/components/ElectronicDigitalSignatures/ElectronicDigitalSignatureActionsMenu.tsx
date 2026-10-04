import { EllipsisVertical } from "lucide-react"
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
