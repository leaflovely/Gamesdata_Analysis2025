<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getGame } from "../api/game";
import { gameStore } from "../store/game";
import { formatDate } from "../utils/dateFormatter";

const router = useRouter();
const game = gameStore();
const currentPage = ref(1);
const pageSize = 24; // 每页24张卡片
const defaultImage = "https://via.placeholder.com/150?text=Game+Image"; // 默认占位图[3](@ref)

// 获取游戏数据
const getGameData = async () => {
  try {
    const res = await getGame();
    game.changeGameData(res);
  } catch (error) {
    console.error("获取游戏数据失败:", error);
  }
};

// 计算当前页显示的游戏
const paginatedGames = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize;
  return game.gameData.slice(startIndex, startIndex + pageSize);
});

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(game.gameData.length / pageSize);
});

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// 处理图片加载错误[3](@ref)
const handleImageError = (event) => {
  event.target.src = defaultImage;
};

// 跳转详情页
const goDetail = (game) => {
  router.push({
    path: "/detail",
    query: { id: game.id },
  });
};

onMounted(() => {
  getGameData();
});
</script>

<template>
  <div class="game-list">
    <div class="game-grid">
      <div
        v-for="game in paginatedGames"
        :key="game.id"
        class="game-card"
        @click="goDetail(game)"
      >
        <div class="card-left">
          <!-- 动态绑定图片src属性[1,2,3](@ref) -->
          <img 
            :src="game.image_url || defaultImage" 
            :alt="game.chinese_name || game.name"
            @error="handleImageError"
          />
        </div>
        <div class="card-right">
          <h3 class="game-title">
            {{ game.chinese_name || game.name }}
          </h3>
          <p class="game-name">{{ game.name }}</p>
          <p class="game-info">
            <span>发行日期: {{ formatDate(game.release_date) }}</span>
          </p>
          <div class="game-scores">
            <div class="score-item">
              <span class="score-label">Meta评分:</span>
              <span class="score-value">{{ game.meta_score }}</span>
            </div>
            <div class="score-item">
              <span class="score-label">用户评分:</span>
              <span class="score-value">{{ game.user_score.toFixed(1) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="pagination">
      <button 
        @click="handlePageChange(currentPage - 1)" 
        :disabled="currentPage === 1"
        class="pagination-button"
      >
        上一页
      </button>
      
      <span class="page-info">
        第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
      </span>
      
      <button 
        @click="handlePageChange(currentPage + 1)" 
        :disabled="currentPage === totalPages"
        class="pagination-button"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<style scoped>
.game-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.game-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.game-card {
  display: flex;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  height: 150px;
}

.game-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.card-left {
  flex: 1;
  max-width: 40%;
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
  font-size: 15px;
  font-weight: bold;
  margin: 0 0 5px 0;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
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

.game-info {
  font-size: 12px;
  color: #777;
  margin: 0 0 8px 0;
}

.game-scores {
  display: flex;
  gap: 15px;
}

.score-item {
  display: flex;
  flex-direction: column;
}

.score-label {
  font-size: 11px;
  color: #888;
}

.score-value {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
}

.pagination-button {
  padding: 8px 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination-button:hover:not(:disabled) {
  background-color: #2980b9;
}

.pagination-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #555;
}
</style>