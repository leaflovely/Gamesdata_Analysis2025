<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getGame } from "../api/game";
import { gameStore } from "../store/game";
import { formatDate } from "../utils/dateFormatter";
import Header from "../components/Header.vue";

const router = useRouter();
const game = gameStore();
const currentPage = ref(1);
const pageSize = 24;
const defaultImage = "https://via.placeholder.com/150?text=Game+Image";

// 筛选相关状态
const platforms = ref(['全部', 'nintendo', 'playstation', 'pc', 'wii', 'xbox']);
const genres = ref(['全部', 'Open-World', 'Action', '3D', 'Fighting', 'Platformer']);
const selectedPlatforms = ref([]);
const selectedGenres = ref([]);
const appliedFilters = ref({ platforms: [], genres: [] });

// 获取游戏数据
const getGameData = async () => {
  try {
    const res = await getGame();
    game.changeGameData(res);
  } catch (error) {
    console.error("获取游戏数据失败:", error);
  }
};

// 处理平台选择
const togglePlatform = (platform) => {
  if (platform === '全部') {
    selectedPlatforms.value = [];
  } else {
    const index = selectedPlatforms.value.indexOf(platform);
    if (index === -1) {
      selectedPlatforms.value.push(platform);
    } else {
      selectedPlatforms.value.splice(index, 1);
    }
    // 如果选择了具体平台，则移除"全部"选项
    if (selectedPlatforms.value.length > 0) {
      const allIndex = selectedPlatforms.value.indexOf('全部');
      if (allIndex !== -1) {
        selectedPlatforms.value.splice(allIndex, 1);
      }
    }
  }
};

// 处理游戏类型选择
const toggleGenre = (genre) => {
  if (genre === '全部') {
    selectedGenres.value = [];
  } else {
    const index = selectedGenres.value.indexOf(genre);
    if (index === -1) {
      selectedGenres.value.push(genre);
    } else {
      selectedGenres.value.splice(index, 1);
    }
    // 如果选择了具体类型，则移除"全部"选项
    if (selectedGenres.value.length > 0) {
      const allIndex = selectedGenres.value.indexOf('全部');
      if (allIndex !== -1) {
        selectedGenres.value.splice(allIndex, 1);
      }
    }
  }
};

// 应用筛选条件
const applyFilters = () => {
  appliedFilters.value = {
    platforms: [...selectedPlatforms.value],
    genres: [...selectedGenres.value]
  };
  currentPage.value = 1; // 重置到第一页
};

// 重置筛选条件
const resetFilters = () => {
  selectedPlatforms.value = [];
  selectedGenres.value = [];
  appliedFilters.value = { platforms: [], genres: [] };
  currentPage.value = 1;
};

// 筛选游戏数据
const filteredGames = computed(() => {
  return game.gameData.filter(game => {
    // 平台筛选
    if (appliedFilters.value.platforms.length > 0) {
      const gamePlatforms = game.platform.toLowerCase().split(',').map(p => p.trim());
      const hasPlatform = appliedFilters.value.platforms.some(platform => 
        gamePlatforms.includes(platform.toLowerCase())
      );
      if (!hasPlatform) return false;
    }
    
    // 游戏类型筛选
    if (appliedFilters.value.genres.length > 0) {
      const gameGenres = game.game_type.split(',').map(g => g.trim());
      const hasGenre = appliedFilters.value.genres.some(genre => 
        gameGenres.includes(genre)
      );
      if (!hasGenre) return false;
    }
    
    return true;
  });
});

// 计算当前页显示的游戏
const paginatedGames = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize;
  return filteredGames.value.slice(startIndex, startIndex + pageSize);
});

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(filteredGames.value.length / pageSize);
});

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// 处理图片加载错误
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
  <Header />
  <div class="game-list">
    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-group">
        <h3>平台</h3>
        <div class="filter-tags">
          <span 
            v-for="platform in platforms" 
            :key="platform"
            :class="{ 'filter-tag': true, 'active': platform === '全部' ? selectedPlatforms.length === 0 : selectedPlatforms.includes(platform) }"
            @click="togglePlatform(platform)"
          >
            {{ platform }}
          </span>
        </div>
      </div>
      
      <div class="filter-group">
        <h3>游戏类型</h3>
        <div class="filter-tags">
          <span 
            v-for="genre in genres" 
            :key="genre"
            :class="{ 'filter-tag': true, 'active': genre === '全部' ? selectedGenres.length === 0 : selectedGenres.includes(genre) }"
            @click="toggleGenre(genre)"
          >
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
    
    <div v-if="filteredGames.length === 0" class="no-results">
      <p>没有找到匹配的游戏</p>
    </div>
    
    <div class="pagination" v-if="totalPages > 1">
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