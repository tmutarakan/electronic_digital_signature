import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { ElectronicDigitalSignaturePublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeleteElectronicDigitalSignature from "./DeleteElectronicDigitalSignature"
import EditElectronicDigitalSignature from "./EditElectronicDigitalSignature"

interface ElectronicDigitalSignatureActionsMenuProps {
  employee: ElectronicDigitalSignaturePublic
}

export const ElectronicDigitalSignatureActionsMenu = ({
  employee,
}: ElectronicDigitalSignatureActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditElectronicDigitalSignature
          employee={employee}
          onSuccess={() => setOpen(false)}
        />
        <DeleteElectronicDigitalSignature
          id={employee.id}
          onSuccess={() => setOpen(false)}
        />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
