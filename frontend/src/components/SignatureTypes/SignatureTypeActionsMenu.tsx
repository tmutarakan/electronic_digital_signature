import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { SignatureTypePublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeleteSignatureType from "./DeleteSignatureType"
import EditSignatureType from "./EditSignatureType"

interface SignatureTypeActionsMenuProps {
  signatureType: SignatureTypePublic
}

export const SignatureTypeActionsMenu = ({
  signatureType,
}: SignatureTypeActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditSignatureType
          signatureType={signatureType}
          onSuccess={() => setOpen(false)}
        />
        <DeleteSignatureType
          id={signatureType.id}
          onSuccess={() => setOpen(false)}
        />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
