import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { CertificationCentersService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import AddCertificationCenter from "@/components/CertificationCenters/AddCertificationCenter"
import { columns } from "@/components/CertificationCenters/columns"
import PendingCertificationCenters from "@/components/Pending/PendingCertificationCenters"

function getCertificationCentersQueryOptions() {
  return {
    queryFn: async () =>
      (
        await CertificationCentersService.centersReadCertificationCenters({
          query: { skip: 0, limit: 100 },
        })
      ).data,
    queryKey: ["certification-centers"],
  }
}

export const Route = createFileRoute("/_layout/certification-centers")({
  component: CertificationCenters,
  head: () => ({
    meta: [
      {
        title: "Certification Centers",
      },
    ],
  }),
})

function CertificationCentersTableContent() {
  const { data: certificationCenters } = useSuspenseQuery(
    getCertificationCentersQueryOptions(),
  )

  if (certificationCenters.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any Certification Centers yet
        </h3>
        <p className="text-muted-foreground">
          Add a new Certification Center to get started
        </p>
      </div>
    )
  }

  return <DataTable columns={columns} data={certificationCenters.data} />
}

function CertificationCentersTable() {
  return (
    <Suspense fallback={<PendingCertificationCenters />}>
      <CertificationCentersTableContent />
    </Suspense>
  )
}

function CertificationCenters() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Certification Center</h1>
          <p className="text-muted-foreground">
            Create and manage your Certification Center
          </p>
        </div>
        <AddCertificationCenter />
      </div>
      <CertificationCentersTable />
    </div>
  )
}
