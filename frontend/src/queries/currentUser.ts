import { UsersService, type UserPublic } from "@/client";

export function getCurrentUserQueryOptions() {
  return {
    queryFn: async (): Promise<UserPublic | null> =>
      (await UsersService.readUserMe()).data,
    queryKey: ["currentUser"] as const,
    staleTime: 5 * 60 * 1000,
  };
}
