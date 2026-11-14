import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"

import useAuth from "@/hooks/useAuth"
import { StatCard, dashboardStatsQueryOptions } from "@/components/Common/StatCard"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
  head: () => ({
    meta: [{ title: "Dashboard - FastAPI Template" }],
  }),
})

function Dashboard() {
  const { user: currentUser } = useAuth()
  const stats = useQuery(dashboardStatsQueryOptions)

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl truncate max-w-sm">
          Hi, {currentUser?.full_name || currentUser?.email || "there"} 👋
        </h1>
        <p className="text-muted-foreground">
          Welcome back, nice to see you again!
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard
          label="Организации"
          value={stats.data?.organizations}
          isLoading={stats.isLoading}
          isError={stats.isError}
        />
        <StatCard
          label="Сотрудники"
          value={stats.data?.employees}
          isLoading={stats.isLoading}
          isError={stats.isError}
        />
        <StatCard
          label="Подписи"
          value={stats.data?.signatures}
          isLoading={stats.isLoading}
          isError={stats.isError}
        />
      </div>
    </div>
  )
}
