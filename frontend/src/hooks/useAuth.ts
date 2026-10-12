import { useQuery } from "@tanstack/react-query";

import type { UserPublic } from "@/client";
import { getCurrentUserQueryOptions } from "@/queries/currentUser";
import useAuthMutations from "./useAuthMutations";

const isLoggedIn = () => {
  return localStorage.getItem("access_token") !== null;
};

const useAuth = () => {
  const mutations = useAuthMutations();

  const { data: user } = useQuery<UserPublic | null, Error>({
    ...getCurrentUserQueryOptions(),
    enabled: isLoggedIn(),
  });

  return {
    ...mutations,
    user,
  };
};

export { isLoggedIn };
export default useAuth;
