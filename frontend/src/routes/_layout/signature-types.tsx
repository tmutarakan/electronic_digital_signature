import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { SignatureTypesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { columns } from "@/components/SignatureTypes/columns"
import AddSignatureType from "@/components/SignatureTypes/AddSignatureType"
import PendingSignatureTypes from "@/components/Pending/PendingSignatureTypes"

function getSignatureTypesQueryOptions() {
  return {
    queryFn: async () =>
      (
        await SignatureTypesService.typesReadSignatureTypes({
          query: { skip: 0, limit: 100 },
        })
      ).data,
    queryKey: ["signature-types"],
  }
}

export const Route = createFileRoute("/_layout/signature-types")({
  component: SignatureTypes,
  head: () => ({
    meta: [
      {
        title: "Signature Types",
      },
    ],
  }),
})

function SignatureTypesTableContent() {
  const { data: certificationCenters } = useSuspenseQuery(
    getSignatureTypesQueryOptions(),
  )

  if (certificationCenters.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any SignatureTypes yet
        </h3>
        <p className="text-muted-foreground">
          Add a new Signature Types to get started
        </p>
      </div>
    )
  }

  return <DataTable columns={columns} data={certificationCenters.data} />
}

function SignatureTypesTable() {
  return (
    <Suspense fallback={<PendingSignatureTypes />}>
      <SignatureTypesTableContent />
    </Suspense>
  )
}

function SignatureTypes() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Signature Types</h1>
          <p className="text-muted-foreground">
            Create and manage your Signature Type
          </p>
        </div>
        <AddSignatureType />
      </div>
      <SignatureTypesTable />
    </div>
  )
}
