<script setup>
import Login from "./Login.vue";
import Register from "./Register.vue";
import { popStore } from "../store/pop";
import { userStore } from "../store/user";
import { useRoute, useRouter } from "vue-router";
import Search from "./Search.vue";

const user = userStore();
const pop = popStore();
const route = useRoute();
const router = useRouter();

const nav_list = [
  { name: "主页", path: "/", icon: "" },
  { name: "可视化", path: "/visualization", icon: "" },
  { name: "全部游戏", path: "/all-games", icon: "" },
  { name: "探索队列", path: "/explore-queue", icon: "" },
  { name: "我的评分", path: "/my-evaluate", icon: "" }
];

const goToPublish = () => {
  if (user.isLogin) {
    router.push('/publish');
  } else {
    pop.changeLoginPop(true);
  }
};
</script>

<template>
  <div class="main-header">
    <div class="header-left">
      <!-- 使用router-link替代a标签 -->
      <router-link to="/" class="header-icon">
        <img src="/images/logo.png" width="100" />
      </router-link>
      
      <!-- 保持原有条件渲染逻辑 -->
      <ul class="header-nav" v-if="!(route.path === '/publish')">
        <li v-for="item in nav_list" :key="item.name">
          <!-- 使用router-link实现SPA导航，但保持原有文字样式 -->
          <router-link :to="item.path">
            {{ item.name }}
          </router-link>
        </li>
      </ul>
    </div>
    
    <Search />
    
    <div class="header-user">
      <!-- 已登录用户菜单 -->
      <el-dropdown v-if="user.isLogin" placement="bottom-end">
        <span class="user-name">{{ user.username }}</span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="router.push('/profile')">
              <i class="el-icon-user"></i> 个人中心
            </el-dropdown-item>
            <el-dropdown-item @click="router.push('/settings')">
              <i class="el-icon-setting"></i> 账户设置
            </el-dropdown-item>
            <el-dropdown-item @click="goToPublish">
              <i class="el-icon-upload"></i> 发布内容
            </el-dropdown-item>
            <el-dropdown-item 
              divided 
              style="color: red" 
              @click="user.logout()"
            >
              <i class="el-icon-switch-button"></i> 退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      
      <!-- 未登录状态 -->
      <el-button 
        v-else 
        plain 
        @click="pop.changeLoginPop(true)"
      >
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
    
    .header-icon {
      display: block;
      height: 60px;
      img {
        height: 100%;
      }
    }
    
    /* 完全保持原有的导航链接CSS样式 */
    .header-nav {
      float: left;
      display: flex;
      line-height: 48px;
      font-size: 14px;
      
      li {
        padding: 0 10px;
        display: flex;
        align-items: center;
        
        a {
          /* 保持原有文字颜色 */
          color: black;
          
          /* 保持原有悬停效果 */
          &:hover {
            color: #fc5531;
          }
        }
      }
    }
  }
  
  .header-user {
    display: flex;
    align-items: center;
    
    /* 保持原有的用户名样式 */
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
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-nav {
    display: none !important;
  }
}
</style>