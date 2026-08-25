import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { OrganizationsService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import AddOrganization from "@/components/Organizations/AddOrganization"
import { columns } from "@/components/Organizations/columns"
import PendingOrganizations from "@/components/Pending/PendingOrganizations"

function getOrganizationsQueryOptions() {
  return {
    queryFn: async () =>
      (
        await OrganizationsService.readOrganizations({
          query: { skip: 0, limit: 100 },
        })
      ).data,
    queryKey: ["organizations"],
  }
}

export const Route = createFileRoute("/_layout/organizations")({
  component: Organizations,
  head: () => ({
    meta: [
      {
        title: "Organizations",
      },
    ],
  }),
})

function OrganizationsTableContent() {
  const { data: organizations } = useSuspenseQuery(
    getOrganizationsQueryOptions(),
  )

  if (organizations.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any organizations yet
        </h3>
        <p className="text-muted-foreground">
          Add a new organization to get started
        </p>
      </div>
    )
  }

  return <DataTable columns={columns} data={organizations.data} />
}

function OrganizationsTable() {
  return (
    <Suspense fallback={<PendingOrganizations />}>
      <OrganizationsTableContent />
    </Suspense>
  )
}

function Organizations() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Organizations</h1>
          <p className="text-muted-foreground">
            Create and manage your organizations
          </p>
        </div>
        <AddOrganization />
      </div>
      <OrganizationsTable />
    </div>
  )
}
