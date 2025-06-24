<script setup>
import icon1 from "../assets/20240829093757.png";
import icon2 from "../assets/20231212032739.png";
import Login from "./Login.vue";
import Register from "./Register.vue";
import { popStore } from "../store/pop";
import { userStore } from "../store/user";
import { useRoute } from "vue-router";
import router from "../router";

const user = userStore();
const pop = popStore();

const location = useRoute();

const nav_list = [
  { name: "主页", url: "#", icon: "" },
  { name: "可视化", url: "#", icon: "" },
  { name: "全部游戏", url: "#", icon: "" },
  { name: "探索队列", url: "#", icon: "" },
  { name: "我的收藏", url: "#", icon: "" }
];
</script>

<template>
  <div class="main-header">
    <div class="header-left">
      <a class="header-icon" href="@/index.html">
        <img src="/images/logo.png" width="100" />
      </a>
      <ul class="header-nav" v-if="!(location.path === '/publish')">
        <li v-for="item in nav_list" :key="item.name">
          <img :src="item.icon" v-if="item.icon ? true : false" />
          <a :href="item.url">{{ item.name }}</a>
        </li>
      </ul>
    </div>
    <div class="header-user">
      <!-- 已登录 -->
      <el-dropdown placement="bottom-end" v-if="user.isLogin">
        <span class="user-name">{{ user.username }}</span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item style="color: red" @click="() => user.logout()"
              >退出登录</el-dropdown-item
            >
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <!-- 未登录 -->
      <el-button plain @click="() => pop.changeLoginPop()" v-else>
        登录
      </el-button>
    </div>
    <Login />
    <Register />
  </div>
</template>

<style scoped lang="less">
::v-deep(.el-dialog__header) {
  display: flex;
  justify-content: center;
}

.main-header {
  width: 100vw;
  height: 65px;
  padding: 0 24px;
  box-shadow: inset 0 -1px 2px #ccc;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: space-between;
  .header-left {
    display: flex;
    align-items: center;
    .back {
      margin-left: 30px;
      display: flex;
      align-items: center;
      cursor: pointer;
    }
    .back :hover {
      color: #409eff;
    }
    .header-icon {
      float: left;
      height: 100%;
      overflow: hidden;
      width: 130px;
      height: 60px;
      img {
        height: 100%;
      }
    }
    .header-nav {
      float: left;
      display: flex;
      line-height: 48px;
      font-size: 14px;
      li {
        padding: 0 10px;
        display: flex;
        align-items: center;
        img {
          width: 20px;
          height: 34px;
        }
        a {
          color: black;
          &:hover {
            color: #fc5531;
          }
        }
      }
    }
  }
  .header-user {
    float: right;
    height: 100%;
    display: flex;
    align-items: center;
    span.user-name {
      display: block;
      width: 32px;
      height: 32px;
      border: 1px solid #ccc;
      border-radius: 50%;
      line-height: 32px;
      text-align: center;
      font-size: 14px;
    }
    .plus-btn {
      background-color: #fc5531;
      width: 80px;
      height: 32px;
      color: white;
      margin-left: 16px;
      &:hover {
        color: white;
      }
      border-radius: 14px;
    }
  }
}
</style>
../store/user
