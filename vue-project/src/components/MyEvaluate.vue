<template>
    <Header />
    <div class="rating-page">
      <!-- 登录提示 -->
      <div v-if="!user.isLogin" class="login-prompt">
        <div class="prompt-card">
          <h2>请登录查看您的游戏评分</h2>
          <p>登录后可以查看和管理您对所有游戏的评分</p>
          <el-button type="primary" @click="openLoginPopup">立即登录</el-button>
        </div>
      </div>
      
      <!-- 用户评分列表 -->
      <div v-else>
        <div class="page-header">
          <h1>我的游戏评分</h1>
          <p>以下是您评价过的所有游戏</p>
        </div>
        
        <!-- 游戏列表 -->
        <div class="game-grid">
            <div
            v-for="ratedGame in ratedGames"
            :key="ratedGame.id"
            class="game-card"
            @click="openDetail(ratedGame)"
            >
            <div class="card-left">
                <img 
                :src="ratedGame.image_url || defaultImage" 
                :alt="ratedGame.chinese_name || ratedGame.name"
                @error="handleImageError"
                />
            </div>
            <div class="card-right">
                <h3 class="game-title">
                {{ ratedGame.chinese_name || ratedGame.name }}
                </h3>
                <p class="game-name">{{ ratedGame.name }}</p>
                <div class="user-rating">
                <span>您的评分:</span>
                <!-- 修改这里：将星星替换为数字显示 -->
                <div class="rating-value">
                    {{ userRating(ratedGame) }}/10
                </div>
                </div>
            </div>
            </div>
        </div>
        
        <div v-if="ratedGames.length === 0" class="no-results">
          <p>您还没有评价任何游戏</p>
          <el-button type="primary" @click="goToAllGames">去评价游戏</el-button>
        </div>
      </div>
      
      <!-- 游戏详情弹窗 -->
      <GameDetailModal 
        :game="selectedGame" 
        :visible="detailVisible"
        :user-rating="selectedUserRating"
        @close="closeDetail"
        @rating-submitted="handleRatingSubmitted"
      />
      
      <!-- 登录弹窗 -->
      <LoginPopup v-if="pop.loginPop" />
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from "vue";
  import { useRouter } from "vue-router";
  import { getGame } from "../api/game";
  import { gameStore } from "../store/game";
  import { userStore } from "../store/user";
  import { popStore } from "../store/pop";
  import Header from "../components/Header.vue";
  import GameDetailModal from "../components/GameDetailModal.vue";
  import LoginPopup from "../components/Login.vue";
  
  const router = useRouter();
  const game = gameStore();
  const user = userStore();
  const pop = popStore();
  const allGames = ref([]);
  const selectedGame = ref(null);
  const detailVisible = ref(false);
  const selectedUserRating = ref(0);
  const defaultImage = "https://via.placeholder.com/150?text=Game+Image";
  
  // 获取所有游戏数据
  const fetchGames = async () => {
    try {
      const res = await getGame();
      allGames.value = res;
      game.changeGameData(res);
    } catch (error) {
      console.error("获取游戏数据失败:", error);
    }
  };
  
  // 获取用户评分的游戏
  const ratedGames = computed(() => {
    if (!user.isLogin || !allGames.value.length) return [];
    
    return allGames.value.filter(game => {
      try {
        const reviews = JSON.parse(game.review_user || "{}");
        return reviews.hasOwnProperty(user.username);
      } catch (e) {
        return false;
      }
    });
  });
  
  // 获取用户对特定游戏的评分
  const userRating = (game) => {
    if (!user.isLogin) return 0;
    
    try {
      const reviews = JSON.parse(game.review_user || "{}");
      return reviews[user.username] || 0;
    } catch (e) {
      return 0;
    }
  };
  
  // 打开游戏详情
  const openDetail = (game) => {
    selectedGame.value = game;
    selectedUserRating.value = userRating(game);
    detailVisible.value = true;
  };
  
  // 关闭详情弹窗
  const closeDetail = () => {
    detailVisible.value = false;
  };
  
  // 处理图片加载错误
  const handleImageError = (event) => {
    event.target.src = defaultImage;
  };
  
  // 处理评分提交
  const handleRatingSubmitted = () => {
    fetchGames(); // 重新获取游戏数据更新列表
    closeDetail();
  };
  
  // 打开登录弹窗
  const openLoginPopup = () => {
    pop.changeLoginPop(true);
  };
  
  // 前往所有游戏页面
  const goToAllGames = () => {
    router.push('/all-games');
  };
  
  // 监听登录状态变化
  watch(() => user.isLogin, (newVal) => {
    if (newVal) {
      fetchGames();
    }
  });
  
  onMounted(() => {
    if (user.isLogin) {
      fetchGames();
    }
  });
  </script>
  
  <style scoped>
  .user-rating {
  display: flex;
  align-items: center; /* 垂直居中 */
  gap: 8px; /* 添加间距 */
}

.rating-value {
  font-size: 18px;
  font-weight: bold;
  color: #ffc107; /* 使用醒目的黄色 */
  background-color: rgba(255, 193, 7, 0.1); /* 浅黄色背景 */
  padding: 4px 10px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加轻微阴影 */
}
  .rating-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .login-prompt {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 70vh;
  }
  
  .prompt-card {
    background: white;
    border-radius: 12px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    max-width: 500px;
    width: 100%;
  }
  
  .prompt-card h2 {
    font-size: 24px;
    margin-bottom: 15px;
    color: #333;
  }
  
  .prompt-card p {
    font-size: 16px;
    color: #666;
    margin-bottom: 25px;
  }
  
  .page-header {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .page-header h1 {
    font-size: 28px;
    margin-bottom: 10px;
    color: #333;
  }
  
  .page-header p {
    font-size: 16px;
    color: #666;
  }
  
  .game-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr); /* 一行显示4个卡片 */
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .game-card {
    display: flex;
    flex-direction: row; /* 左右布局 */
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    height: 140px; /* 适当增加高度 */
  }
  
  .game-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
  
  .card-left {
    flex: 0 0 40%; /* 左侧固定40%宽度 */
    overflow: hidden;
  }
  
  .card-left img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  
  .card-right {
    flex: 1;
    padding: 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .game-title {
    font-size: 16px;
    font-weight: bold;
    margin: 0 0 5px 0;
    color: #333;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* 限制为两行 */
    -webkit-box-orient: vertical;
  }
  
  .game-name {
  font-size: 12px;
  color: #666;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
}
  
  .user-rating {
    display: flex;
    flex-direction: column;
  }
  
  .user-rating span {
    font-size: 12px;
    color: #666;
    margin-bottom: 5px;
  }
  
  .stars {
    display: flex;
    line-height: 1;
  }
  
  .star {
    font-size: 16px;
    color: #ccc;
    margin-right: 1px;
  }
  
  .star-filled {
    color: #ffc107; /* 黄色星星 */
  }
  
  .no-results {
    text-align: center;
    padding: 40px 0;
    font-size: 16px;
    color: #666;
  }
  
  .no-results .el-button {
    margin-top: 15px;
  }
  
  /* 响应式调整 */
  @media (max-width: 1200px) {
    .game-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  
  @media (max-width: 900px) {
    .game-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  @media (max-width: 600px) {
    .game-grid {
      grid-template-columns: 1fr;
    }
    
    .game-card {
      height: 120px;
    }
  }
  </style>