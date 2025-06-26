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
  return request({ method: "get", url: "/game/get" }); // 恢复为获取全部游戏数据
};

/**
 * 分页获取游戏数据
 * @param {number} page 当前页码
 * @param {number} pageSize 每页数据量
 * @returns {Promise<Array>} 游戏数据
 */
export const getGameByPage = async (page, pageSize) => {
  return request({ method: "get", url: `/game/get?page=${page}&pageSize=${pageSize}` });
};

