import request from "../utils/request";

/**
 * 游戏搜索接口
 */
export const searchGame = (data) => {
  return request({ method: "post", url: "/game/search", data });
};

/**
 * 游戏获取接口
 */
export const getGame = () => {
  return request({ method: "get", url: "/game/get" });
};

