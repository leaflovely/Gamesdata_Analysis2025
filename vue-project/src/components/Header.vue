<script setup>
import Login from "./Login.vue";
import Register from "./Register.vue";
import { popStore } from "../store/pop";
import { userStore } from "../store/user";
import { useRoute, useRouter } from "vue-router";
import { computed } from "vue";

const user = userStore();
const pop = popStore();
const route = useRoute();
const router = useRouter();

const nav_list = [
  { name: "主页", path: "/", icon: "el-icon-house" },
  { name: "可视化", path: "/visualization", icon: "el-icon-data-analysis" },
  { name: "全部游戏", path: "/all-games", icon: "el-icon-menu" },
  { name: "探索队列", path: "/explore-queue", icon: "el-icon-search" },
  { name: "我的评分", path: "/my-evaluate", icon: "el-icon-star-on" }
];

const goToPublish = () => {
  if (user.isLogin) {
    router.push('/publish');
  } else {
    pop.changeLoginPop(true);
  }
};

const userMenu = computed(() => [
  //{ label: "个人中心", icon: "el-icon-user", action: () => router.push('/profile') },
  //{ label: "账户设置", icon: "el-icon-setting", action: () => router.push('/settings') },
  //{ label: "发布内容", icon: "el-icon-upload", action: goToPublish },
  { label: "退出登录", icon: "el-icon-switch-button", action: user.logout, danger: true }
]);
</script>

<template>
  <div class="sidebar-header">
    <div class="sidebar-logo">
      <router-link to="/">
        <div class="logo-circle">
          <img src="/src/assets/logo.png" alt="logo" />
        </div>
      </router-link>
    </div>
    <div class="sidebar-nav">
      <el-button
        v-for="item in nav_list"
        :key="item.name"
        :type="route.path === item.path ? 'primary' : 'default'"
        class="nav-btn"
        @click="router.push(item.path)"
        :icon="item.icon"
        round
      >
        {{ item.name }}
      </el-button>
    </div>
    <div class="sidebar-user">
      <template v-if="user.isLogin">
        <el-dropdown placement="right-start">
          <el-button class="user-btn" type="primary" round>
            <i class="el-icon-user"></i>
            {{ user.username }}
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item
                v-for="menu in userMenu"
                :key="menu.label"
                :style="{ color: menu.danger ? 'red' : '' }"
                @click="menu.action"
              >
                <i :class="menu.icon"></i> {{ menu.label }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
      <template v-else>
        <el-button
          type="primary"
          class="nav-btn"
          round
          @click="pop.changeLoginPop(true)"
        >
          登录
        </el-button>
      </template>
    </div>
    <Login />
    <Register />
  </div>
</template>

<style scoped lang="less">
.sidebar-header {
  position: fixed;
  left: 0;
  top: 0;
  width: 300px;
  height: 100vh;
  background: transparent;
  //box-shadow: 2px 0 12px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 0 24px 0;
  z-index: 100;
  transition: width 0.2s;

.sidebar-logo {
  margin-bottom: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
  .logo-circle {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #d3ff87 0%, #8bcd17 100%);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4px 16px #e8ffc0;
    transition: box-shadow 0.2s;
    &:hover {
      box-shadow: 0 8px 24px #d3ff87;
    }
    img {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      object-fit: cover;
      background: #fff;
      box-shadow: 0 2px 8px rgba(0,0,0,0.10);
    }
  }
}

  .sidebar-nav {
    flex: 1;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 30px;
    align-items: center;

    .nav-btn {
      width: 100%;
      color: #fff;
      //background: linear-gradient(90deg, #fc5531 0%, #fc8c31 100%);
      border: none;
      font-weight: 500;
      border-radius: 8px;
      height: 48px;
      font-size: 40px;
      letter-spacing: 1px;
      box-shadow: 0 2px 8px rgba(252,85,49,0.08);
      transition: background 0.2s;
      &:hover {
        //background: linear-gradient(90deg, #fc8c31 0%, #fc5531 100%);
        color: #9b6cfb;
      }
    }
    .el-button--default {
      margin-left: -40px; 
      background: transparent;
      color: #fff;
      border: 0px solid #fff2;
    }
    .el-button--primary {
      margin-left: -20px; 
      background: transparent;
      //background: linear-gradient(90deg, #fc5531 0%, #fc8c31 100%);
      color: #9b6cfb;
    }
  }

  .sidebar-user {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 24px;

    .user-btn {
      width: 80%;
      color: #fff !important;
      background: #081641 ;
      border: 1px solid #fff2;
      font-size: 20px;
      margin-bottom: 100px;
      &:hover {
        background: #2fe4cc;
        color: #fff;
      }
    }
  }
}

/* 响应式收缩 */
@media (max-width: 900px) {
  .sidebar-header {
    width: 64px;
    padding: 16px 0;
    .sidebar-logo img { width: 40px; }
    .sidebar-nav .nav-btn,
    .sidebar-user .user-btn {
      width: 40px;
      font-size: 0;
      padding: 0;
      justify-content: center;
      i { font-size: 20px; }
      span { display: none; }
    }
  }
}
</style>