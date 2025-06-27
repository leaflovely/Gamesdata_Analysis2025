<script setup>
import Login from "./Login.vue";
import Register from "./Register.vue";
import { popStore } from "../store/pop";
import { userStore } from "../store/user";
import { useRoute, useRouter } from "vue-router";
import { computed, ref } from "vue";
import GameAgent from './game_agent.vue'; // 导入AI助手组件

const user = userStore();
const pop = popStore();
const route = useRoute();
const router = useRouter();
const isCollapsed = ref(false);

const nav_list = [
  { name: "主页", path: "/", icon: "el-icon-house" },
  { name: "可视化", path: "/visualization", icon: "el-icon-data-analysis" },
  { name: "全部游戏", path: "/all-games", icon: "el-icon-menu" },
  { name: "探索队列", path: "/explore-queue", icon: "el-icon-search" },
  { name: "我的评分", path: "/my-evaluate", icon: "el-icon-star-on" }
];

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
  document.documentElement.style.setProperty('--sidebar-width', isCollapsed.value ? '80px' : '300px');
};

const goToPublish = () => {
  if (user.isLogin) {
    router.push('/publish');
  } else {
    pop.changeLoginPop(true);
  }
};

const userMenu = computed(() => [
  { label: "退出登录", icon: "el-icon-switch-button", action: user.logout, danger: true }
]);
</script>

<template>
  <div class="sidebar-header" :class="{ 'collapsed': isCollapsed }">
    <div class="sidebar-top">
      <div class="sidebar-logo">
        <router-link to="/">
          <div class="logo-circle">
            <img src="/src/assets/logo.png" alt="logo" />
          </div>
        </router-link>
        <span class="logo-text" v-show="!isCollapsed">专业的游戏评分网站</span>
      </div>
      <!-- 移除原el-button collapse-btn -->
    </div>
    <!-- 新的收放按钮，绝对定位在右上角 -->
    <button class="custom-collapse-btn" @click="toggleSidebar">
      <svg :style="{ transform: isCollapsed ? 'rotate(180deg)' : 'rotate(0deg)' }" width="28" height="28"
        viewBox="0 0 28 28">
        <polyline points="10,8 18,14 10,20" fill="none" stroke="#9b6cfb" stroke-width="2.5" stroke-linecap="round"
          stroke-linejoin="round" />
      </svg>
    </button>
    <div class="divider"></div>

    <div class="sidebar-nav">
      <el-button v-for="item in nav_list" :key="item.name" :type="route.path === item.path ? 'primary' : 'default'"
        class="nav-btn" @click="router.push(item.path)" :icon="item.icon" round>
        <span v-show="!isCollapsed">{{ item.name }}</span>
      </el-button>
    </div>

    <div class="sidebar-user">
      <template v-if="user.isLogin">
        <el-dropdown placement="right-start">
          <el-button class="user-btn" type="primary" round>
            <i class="el-icon-user"></i>
            <span v-show="!isCollapsed">{{ user.username }}</span>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-for="menu in userMenu" :key="menu.label" :style="{ color: menu.danger ? 'red' : '' }"
                @click="menu.action">
                <i :class="menu.icon"></i> {{ menu.label }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
      <template v-else>
        <el-button type="primary" class="nav-btn" round @click="pop.changeLoginPop(true)">
          <span v-show="!isCollapsed">登录</span>
          <i v-show="isCollapsed" class="el-icon-user"></i>
        </el-button>
      </template>
    </div>
    <Login />
    <Register />
    <!-- 添加AI助手组件 -->
    <div class="game-agent-wrapper">
      <GameAgent />
    </div>
  </div>
</template>

<style scoped lang="less">
:root {
  --sidebar-width: 300px;
}

.sidebar-header {
  position: fixed;
  left: 0;
  top: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  z-index: 100;
  transition: all 0.3s ease;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);

  &.collapsed {
    .sidebar-logo {
      justify-content: center;
    }

    .nav-btn {
      justify-content: center;

      span {
        display: none;
      }
    }
  }

  .sidebar-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
  }

  .custom-collapse-btn {
    position: absolute;
    top: 0;
    right: -40px; // 使按钮最左侧与侧边栏最右侧贴合
    width: 40px;
    height: 40px;
    background: rgba(155, 108, 251, 0.18);
    border: none;
    border-top-right-radius: 40px;
    border-bottom-right-radius: 40px;
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.10);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 102;
    transition: background 0.2s;
    outline: none;

    &:hover {
      background: rgba(155, 108, 251, 0.35);
    }

    svg {
      transition: transform 0.3s;
      display: block;
      width: 20px;
      height: 20px;
    }
  }

  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    margin: 20px 0;
  }

  .sidebar-logo {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    transition: all 0.3s ease;

    .logo-circle {
      width: 50px;
      height: 50px;
      min-width: 50px;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      background: transparent;
      animation: pulse 2s infinite ease-in-out;

      // 扩散光圈
      &::after {
        content: '';
        position: absolute;
        left: 50%;
        top: 50%;
        width: 54px;
        height: 54px;
        border-radius: 50%;
        transform: translate(-50%, -50%) scale(1);
        background: radial-gradient(circle, rgba(94, 233, 149, 0.28) 0%, rgba(0, 255, 231, 0.12) 60%, rgba(255, 255, 255, 0) 85%);
        z-index: 0;
        pointer-events: none;
        animation: logo-glow-ring 1.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      }

      img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        background: #fff;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.10);
        position: relative;
        z-index: 1;
      }
    }

    .logo-text {
      color: white;
      font-size: 18px;
      margin-left: 10px;
      white-space: nowrap;
      font-family: 'Orbitron', sans-serif;
      letter-spacing: 1px;
      text-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
    }
  }

  .sidebar-nav {
    flex: 1;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 0 0; // 移除左右padding
    overflow-y: auto;

    .nav-btn {
      width: 100%;
      color: #fff;
      background: transparent;
      border: none;
      font-weight: 600;
      border-radius: 0;
      height: 60px;
      font-size: 22px;
      display: flex;
      align-items: center;
      justify-content: flex-start; // 左对齐
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
      transition: all 0.3s ease;
      box-shadow: none;
      margin: 0;
      padding-left: 0;
      padding-right: 0;
      padding-top: 0;
      padding-bottom: 0;
      padding-inline-start: 0;
      padding-inline-end: 0;

      &:hover {
        color: #9b6cfb;
        background: rgba(155, 108, 251, 0.08);
        transform: none;
      }

      &.el-button--primary {
        color: #9b6cfb;
        background: transparent;
        border: none;
      }

      i {
        margin-right: 10px;
      }
    }

    .el-button--default {
      background: transparent;
      color: #fff;
      border: none;
      box-shadow: none;
    }

    .el-button--primary {
      background: transparent;
      color: #9b6cfb;
      border: none;
      box-shadow: none;
    }
  }

  .sidebar-user {
    width: 100%;
    padding: 0 15px;
    margin-top: auto;

    .user-btn {
      width: 100%;
      color: #fff !important;
      background: rgba(8, 22, 65, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      font-size: 16px;
      margin-bottom: 20px;
      padding: 0 20px;
      justify-content: flex-start;

      &:hover {
        background: rgba(47, 228, 204, 0.7);
      }

      i {
        margin-right: 10px;
      }
    }
  }
}

/* 添加AI助手容器样式 */
.game-agent-wrapper {
  position: fixed;
  right: 20px;
  bottom: 20px;
  width: 400px;
  height: 600px;
  z-index: 1000;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.05);
  }

  100% {
    transform: scale(1);
  }
}

@keyframes logo-glow-ring {
  0% {
    opacity: 0.6;
    transform: translate(-50%, -50%) scale(1);
  }

  80% {
    opacity: 0.15;
    transform: translate(-50%, -50%) scale(1.35);
  }

  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(1.45);
  }
}
</style>