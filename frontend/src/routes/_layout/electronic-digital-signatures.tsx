import { useSuspenseQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { Search } from "lucide-react";
import { Suspense, useMemo } from "react";

import { ElectronicDigitalSignaturesService } from "@/client";
import { DataTable } from "@/components/Common/DataTable";
import AddElectronicDigitalSignature from "@/components/ElectronicDigitalSignatures/AddElectronicDigitalSignature";
import { getColumns } from "@/components/ElectronicDigitalSignatures/columns";
//import PendingElectronicDigitalSignatures from "@/components/Pending/PendingElectronicDigitalSignatures"
import { LoadingSpinner } from "@/components/Common/LoadingSpinner";

function getElectronicDigitalSignaturesQueryOptions() {
  return {
    queryFn: async () =>
      (
        await ElectronicDigitalSignaturesService.digitalSignaturesReadElectronicDigitalSignatures(
          {
            query: { skip: 0, limit: 100 },
          },
        )
      ).data,
    queryKey: ["electronic-digital-signatures"],
  };
}

export const Route = createFileRoute("/_layout/electronic-digital-signatures")({
  component: ElectronicDigitalSignatures,
  head: () => ({
    meta: [
      {
        title: "Electronic Digital Signatures",
      },
    ],
  }),
});

function ElectronicDigitalSignaturesTableContent() {
  const { data: electronicDigitalSignatures } = useSuspenseQuery(
    getElectronicDigitalSignaturesQueryOptions(),
  );
  const { user } = Route.useRouteContext()
  const isSuperuser = user?.is_superuser ?? false
  const columns = useMemo(() => getColumns(isSuperuser), [isSuperuser])

  if (electronicDigitalSignatures.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any Electronic Digital Signatures yet
        </h3>
        <p className="text-muted-foreground">
          {isSuperuser
            ? "Add a new electronic digital signature to get started"
            : "Signatures will appear here once added"}
        </p>
      </div>
    );
  }

  return (
    <DataTable columns={columns} data={electronicDigitalSignatures.data} />
  );
}

function ElectronicDigitalSignaturesTable() {
  return (
    <Suspense
      fallback={
        <LoadingSpinner label="Loading Electronic Digital Signatures" />
      }
    >
      <ElectronicDigitalSignaturesTableContent />
    </Suspense>
  );
}

function ElectronicDigitalSignatures() {
  const { user } = Route.useRouteContext()
  const isSuperuser = user?.is_superuser ?? false

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">
            Electronic Digital Signature
          </h1>
          <p className="text-muted-foreground">
            Create and manage your Electronic Digital Signature
          </p>
        </div>
        {isSuperuser && <AddElectronicDigitalSignature />}
      </div>
      <ElectronicDigitalSignaturesTable />
    </div>
  );
}
