<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getGameByPage } from "../api/game"; // 修改为分页获取游戏数据的 API
import { gameStore } from "../store/game";
import { formatDate } from "../utils/dateFormatter";
import Search from "./Search.vue";
import Header from "../components/Header.vue";
import GameDetailModal from "../components/GameDetailModal.vue"; // 引入详情弹窗组件

const router = useRouter();
const game = gameStore();
const currentPage = ref(1);
const pageSize = 24; // 每页24张卡片
const defaultImage = "https://via.placeholder.com/150?text=Game+Image"; // 默认占位图

// 详情弹窗控制状态
const detailVisible = ref(false);
const selectedGame = ref(null);

// 获取游戏数据（分页）
const getGameData = async (page) => {
  try {
    const res = await getGameByPage(page, pageSize); // 调用分页 API
    game.changeGameData(res);
  } catch (error) {
    console.error("获取游戏数据失败:", error);
  }
};

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page;
  getGameData(page); // 根据当前页获取数据
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// 处理图片加载错误
const handleImageError = (event) => {
  event.target.src = defaultImage;
};

// 打开详情弹窗
const openDetail = (game) => {
  selectedGame.value = game;
  detailVisible.value = true;
};

// 关闭详情弹窗
const closeDetail = () => {
  detailVisible.value = false;
};

onMounted(() => {
  getGameData(currentPage.value); // 初次加载时获取第一页数据
});
</script>

<template>
  <Header />
  <div class="game-list">
    <!-- 筛选区域 -->
    <Search class="search-bar" />
    <div class="filter-section">
      <div class="filter-group">
        <h3>平台</h3>
        <div class="filter-tags">
          <span v-for="platform in platforms" :key="platform"
            :class="{ 'filter-tag': true, 'active': platform === '全部' ? selectedPlatforms.length === 0 : selectedPlatforms.includes(platform) }"
            @click="togglePlatform(platform)">
            {{ platform }}
          </span>
        </div>
      </div>

      <div class="filter-group">
        <h3>游戏类型</h3>
        <div class="filter-tags">
          <span v-for="genre in genres" :key="genre"
            :class="{ 'filter-tag': true, 'active': genre === '全部' ? selectedGenres.length === 0 : selectedGenres.includes(genre) }"
            @click="toggleGenre(genre)">
            {{ genre }}
          </span>
        </div>
      </div>

      <div class="filter-actions">
        <button class="filter-button" @click="applyFilters">查询</button>
        <button class="filter-button reset" @click="resetFilters">重置</button>
      </div>
    </div>

    <!-- 游戏列表 -->
    <div class="game-grid">
      <div v-for="game in game.gameData" :key="game.id" class="game-card" @click="openDetail(game)">
        <div class="card-left">
          <img :src="game.image_url || defaultImage" :alt="game.chinese_name || game.name" @error="handleImageError" />
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
      <button @click="handlePageChange(currentPage - 1)" :disabled="currentPage === 1" class="pagination-button">
        上一页
      </button>

      <span class="page-info">
        第 {{ currentPage }} 页
      </span>
      <span class="page-info">
        共548页
      </span>
      <button @click="handlePageChange(currentPage + 1)" class="pagination-button">
        下一页
      </button>
    </div>

    <!-- 游戏详情弹窗组件 -->
    <GameDetailModal :game="selectedGame" :visible="detailVisible" @close="closeDetail" />
  </div>
</template>

<style scoped>
.game-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  margin-left: 400px;
}

.search-bar {
  margin-bottom: 24px;
}

/* 筛选区域样式 */
.filter-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.filter-group {
  margin-bottom: 20px;
}

.filter-group h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 12px;
  font-weight: 600;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-tag {
  padding: 8px 16px;
  background-color: #f5f5f5;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  color: #666;
  border: 1px solid #e0e0e0;
}

.filter-tag:hover {
  background-color: #e9e9e9;
  transform: translateY(-2px);
}

.filter-tag.active {
  background-color: #3498db;
  color: white;
  border-color: #3498db;
  font-weight: 500;
}

.filter-actions {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.filter-button {
  padding: 8px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 14px;
}

.filter-button:hover {
  background-color: #2980b9;
}

.filter-button.reset {
  background-color: #95a5a6;
}

.filter-button.reset:hover {
  background-color: #7f8c8d;
}

/* 游戏列表样式 */
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

/* 无结果提示 */
.no-results {
  text-align: center;
  padding: 40px 0;
  font-size: 16px;
  color: #666;
}

/* 分页样式 */
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

/* 响应式调整 */
@media (max-width: 1024px) {
  .game-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .game-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-tags {
    gap: 8px;
  }

  .filter-tag {
    padding: 6px 12px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .game-grid {
    grid-template-columns: 1fr;
  }

  .filter-tags {
    gap: 6px;
  }

  .filter-tag {
    padding: 5px 10px;
    font-size: 12px;
  }
}
</style>