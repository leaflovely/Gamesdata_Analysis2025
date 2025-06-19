import request from "../utils/request";

/**
 * 注册接口
 */
export const getRegister = (data) => {
  return request({ method: "post", url: "/user/register", data });
};

/**
 * 登录接口
 */
export const getLogin = (data) => {
  return request({ method: "post", url: "/user/login", data });
};
