<script setup>
import Header from "../components/Header.vue";
import Search from "../components/Search.vue";
//import ExploreLite from "../components/ExploreLite.vue"; 

import OtherList from "../components/OtherList.vue";
import { ref } from "vue";
import CarouselWithDetail from '../components/CarouselWithDetail.vue'
import GameAgent from '../components/game_agent.vue' // 添加导入
import Login from '../components/Login.vue'; // 新增导入
import Register from '../components/Register.vue'; // 新增导入
import { popStore } from '../store/pop'; // 新增导入
import { userStore } from '../store/user'; // 新增导入

const activeName = ref("second");
const pop = popStore();
const user = userStore();
</script>

<template>
  <!-- 首页内容 -->
  <Login />
  <Register />
  <!-- 右上角登录按钮，仅未登录时显示 -->
  <button
    v-if="!user.isLogin"
    class="login-btn-topright"
    @click="pop.changeLoginPop(true)"
  >
    登录
  </button>
  <Header />
  <div class="custom-gap"></div>
  <main>
    <div class="main-box">
      <Search />
      <div class="carousel-tip">
        游戏推荐 ———来自我们编辑的精选
      </div>
      <CarouselWithDetail />
      <!-- 添加 AI 助手组件 -->
      <div class="agent-section">
        <h2 class="section-title">游戏助手</h2>
        <GameAgent />
      </div>
    </div>
  </main>
</template>

<style lang="less">
body {
  min-height: 100vh;
  /* 动态背景渐变 */
  background: linear-gradient(135deg, #d403e1 0%, #00465a 30%, #2360b3 70%, #6f3692 100%);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

.custom-gap {
  height: 32px;
  background: transparent;
}

/* 右上角登录按钮样式 */
.login-btn-topright {
  position: fixed;
  top: 32px;
  right: 48px;
  z-index: 2001;
  background: linear-gradient(90deg, #1de9b6 0%, #1dc8e9 100%);
  color: #fff;
  border: none;
  border-radius: 24px;
  font-size: 20px;
  font-weight: 600;
  padding: 12px 36px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.10);
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
  outline: none;
}
.login-btn-topright:hover {
  background: linear-gradient(90deg, #1de9b6 0%, #00e0ff 100%);
  color: #fff;
}

main {
  background-color: transparent;
  overflow: hidden;

  .main-box {
    width: 1200px;
    margin: 0 auto;
    margin-left: 400px; // 新增，向右平移80px
  }

  .carousel-tip {
    color: #fff;
    font-size: 40px;
    margin-top: 20px;
    margin-bottom: 0 auto;
    text-align: left;
    letter-spacing: 1px;
    font-weight: 500;
    text-shadow:
      5px 5px 12px rgba(0, 0, 0, 0.55), // 主黑色阴影更深更大
      0 6px 24px rgba(59, 130, 246, 0.28), // 蓝色柔光更明显
      2px 2px 0 #222; // 细实线阴影增强立体
  }

  .section-title {
    color: #fff;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 20px;
    margin-top: 20px;
    letter-spacing: 2px;
  }

  .logo {
    display: block;
    width: 213px;
    height: 100px;
    margin: 0 auto;
  }

  .search-box {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }

  .demo-tabs>.el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
  }

  /* 添加助手组件样式 */
  .agent-section {
    margin-top: 40px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    backdrop-filter: blur(10px);
  }

  .section-title {
    color: #fff;
    font-size: 28px;
    margin-bottom: 20px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
}

/* 新增：让登录/注册弹窗居中显示 */
:deep(.el-dialog__wrapper) {
  display: flex !important;
  align-items: center;
  justify-content: center;
  z-index: 3000 !important;
}

:deep(.el-dialog) {
  margin: 0 auto !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  position: relative !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>