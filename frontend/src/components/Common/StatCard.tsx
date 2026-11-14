import { DashboardService } from "@/client"

export const dashboardStatsQueryOptions = {
  queryKey: ["dashboard", "stats"],
  queryFn: async () =>
    (await DashboardService.readDashboardStats()).data,
}

interface StatCardProps {
  label: string
  value?: number
  isLoading?: boolean
  isError?: boolean
}

export function StatCard({ label, value, isLoading, isError }: StatCardProps) {
  return (
    <div className="rounded-lg border bg-card p-6">
      <p className="text-sm text-muted-foreground">{label}</p>
      <p className="text-3xl font-bold tracking-tight mt-2">
        {isLoading ? (
          <span className="text-muted-foreground">…</span>
        ) : isError ? (
          <span className="text-destructive">—</span>
        ) : (
          (value ?? 0).toLocaleString("ru-RU")
        )}
      </p>
    </div>
  )
}
