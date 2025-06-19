import axios from "axios";

/**
 * 创建axios实例
 */
const service = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: "3000",
});

/**
 * 请求拦截
 */
service.interceptors.request.use((config) => {
  if (config.url.indexOf("publish") >= 0) {
    config.headers.authorization = localStorage.getItem("token");
  }
  return config;
});

/**
 * 响应拦截
 */
service.interceptors.response.use((res) => {
  const { code, data, message, access } = res.data;
  if (code === 200) {
    return data || message;
  }
  if (access) {
    return access;
  }
});

/**
 * 封装请求函数
 */
const request = (options) => {
  if (options.method === "get") {
    options.params = options.data;
  }
  return service(options);
};

export default request;
