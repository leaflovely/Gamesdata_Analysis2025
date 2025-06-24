import request from "../utils/request";

/**
 * 文章搜索接口
 */
export const searchGame = (data) => {
  return request({ method: "post", url: "/game/search", data });
};

/**
 * 文章获取接口
 */
export const getGame = () => {
  return request({ method: "get", url: "/game/get" });
};

