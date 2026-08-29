import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { CertificationCenterPublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeleteCertificationCenter from "./DeleteCertificationCenter"
import EditCertificationCenter from "./EditCertificationCenters"

interface CertificationCenterActionsMenuProps {
  certificationCenter: CertificationCenterPublic
}

export const CertificationCenterActionsMenu = ({
  certificationCenter,
}: CertificationCenterActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditCertificationCenter
          certificationCenter={certificationCenter}
          onSuccess={() => setOpen(false)}
        />
        <DeleteCertificationCenter
          id={certificationCenter.id}
          onSuccess={() => setOpen(false)}
        />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
