import { defineStore } from "pinia";
import { ref } from "vue";

export const userStore = defineStore(
  "user",
  () => {
    // 账号名
    const username = ref("");

    // 是否登录
    const isLogin = ref(false);

    // 登录
    const getLoginInfo = () => {
      isLogin.value = true;
    };

    const changeUsername = (u) => {
      username.value = u;
    };

    // 退出登录
    const logout = () => {
      isLogin.value = false;
      username.value = "";
      localStorage.removeItem("token");
    };

    return { username, isLogin, changeUsername, getLoginInfo, logout };
  },
  {
    persist: true, //Store中数据持久化生效
  }
);
