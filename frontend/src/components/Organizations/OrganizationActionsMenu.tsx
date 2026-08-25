import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { OrganizationPublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeleteOrganization from "../Organizations/DeleteOrganization"
import EditOrganization from "../Organizations/EditOrganization"

interface OrganizationActionsMenuProps {
  organization: OrganizationPublic
}

export const OrganizationActionsMenu = ({
  organization,
}: OrganizationActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditOrganization
          organization={organization}
          onSuccess={() => setOpen(false)}
        />
        <DeleteOrganization
          id={organization.id}
          onSuccess={() => setOpen(false)}
        />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
