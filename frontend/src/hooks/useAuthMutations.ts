import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";

import {
  type Body_login_login_access_token as AccessToken,
  LoginService,
  type UserRegister,
  UsersService,
} from "@/client";
import { handleError } from "@/utils";
import useCustomToast from "./useCustomToast";

const useAuthMutations = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { showErrorToast } = useCustomToast();

  const signUpMutation = useMutation({
    mutationFn: (data: UserRegister) =>
      UsersService.registerUser({ body: data }),
    onSuccess: () => {
      navigate({ to: "/login" });
    },
    onError: handleError.bind(showErrorToast),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const login = async (data: AccessToken) => {
    const response = await LoginService.loginAccessToken({ body: data });
    localStorage.setItem("access_token", response.data.access_token);
  };

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: () => {
      // убираем возможный null из кэша, чтобы _layout сделал свежий запрос
      queryClient.removeQueries({ queryKey: ["currentUser"] });
      navigate({ to: "/" });
    },
    onError: handleError.bind(showErrorToast),
  });

  const logout = () => {
    localStorage.removeItem("access_token");
    queryClient.clear();
    navigate({ to: "/login" });
  };

  return {
    signUpMutation,
    loginMutation,
    logout,
  };
};

export default useAuthMutations;
