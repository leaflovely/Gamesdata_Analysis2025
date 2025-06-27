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

/**
 * 游戏筛选接口
 * @param {Object} filters 筛选条件
 * @returns {Promise<Array>} 筛选后的游戏数据
 */
export const filterGames = async (filters) => {
  console.log('发送筛选请求，参数:', filters); // 添加请求日志
  const response = await request({
    method: "post",
    url: "/game/filter",
    data: filters,
  });
  console.log('收到筛选响应:', response); // 添加响应日志
  return response;
};

