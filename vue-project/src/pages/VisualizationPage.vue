<script>
import { ref, onMounted, computed } from 'vue';
import Papa from 'papaparse';
import MetaScoreDistribution from '../components/MetaScoreDistribution.vue';
import UserScoreDistribution from '../components/UserScoreDistribution.vue';
import MetaReviewRatio from '../components/MetaReviewRatio.vue';
import UserReviewRatio from '../components/UserReviewRatio.vue';
import ReleaseTrend from '../components/ReleaseTrend.vue';
import GameTypeDistribution from '../components/GameTypeDistribution.vue';
import DeveloperPublisherStats from '../components/DeveloperPublisherStats.vue';
import DeveloperScoreStability from '../components/DeveloperScoreStability.vue';
import Header from "../components/Header.vue";

export default {
  components: {
    MetaScoreDistribution,
    UserScoreDistribution,
    MetaReviewRatio,
    UserReviewRatio,
    ReleaseTrend,
    GameTypeDistribution,
    DeveloperPublisherStats,
    DeveloperScoreStability,
    Header
  },
  setup() {
    const gameData = ref([]);
    const selectedType = ref('');
    const topTypes = ref([]);
    const selectedPublisher = ref('');
    const topPublishers = ref([]);

    // 统计出现频率最高的6个游戏类型
    function getTopTypes(data) {
      const typeCount = {};
      data.forEach(item => {
        const types = (item.Genres || '').split(/[,，;]/).map(t => t.trim()).filter(Boolean);
        types.forEach(type => {
          typeCount[type] = (typeCount[type] || 0) + 1;
        });
      });
      return Object.entries(typeCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6)
        .map(([type]) => type);
    }

    // 统计出现频率最高的6个发行商
    function getTopPublishers(data) {
      const publisherCount = {};
      data.forEach(item => {
        const publisher = item.Publisher;
        if (publisher) {
          publisherCount[publisher] = (publisherCount[publisher] || 0) + 1;
        }
      });
      return Object.entries(publisherCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6)
        .map(([publisher]) => publisher);
    }

    onMounted(() => {
      Papa.parse('/visualization_game_data.csv', {
        download: true,
        header: true,
        complete: (results) => {
          gameData.value = results.data;
          topTypes.value = getTopTypes(results.data);
          topPublishers.value = getTopPublishers(results.data);
        }
      });
    });

    // 根据选择的类型筛选数据
    const filteredGameData = computed(() => {
      if (!selectedType.value) return gameData.value;
      return gameData.value.filter(item => {
        const types = (item.Genres || '').split(/[,，;]/).map(t => t.trim());
        return types.includes(selectedType.value);
      });
    });

    // 根据选择的发行商筛选数据
    const filteredPublisherData = computed(() => {
      if (!selectedPublisher.value.length) return gameData.value;
      return gameData.value.filter(item => selectedPublisher.value.includes(item.Publisher));
    });

    return { 
      gameData, 
      filteredGameData, 
      filteredPublisherData,
      selectedType, 
      selectedPublisher,
      topTypes,
      topPublishers 
    };
  }
};
</script>
<template>
  <Header /> 

  <div class="visualization-page">
    <h1>游戏数据分析可视化</h1>
    <!-- 筛选标签 -->

      <h2 class="section-title">评分与评价分析</h2> 
    <div class="type-filter">
      <span style="color: #fff;">筛选类型：</span>
      <button
        v-for="type in topTypes"
        :key="type"
        :class="{ active: selectedType === type }"
        @click="selectedType = (selectedType === type ? '' : type)"
      >{{ type }}</button>
      <button
        :class="{ active: !selectedType }"
        @click="selectedType = ''"
      >全部</button>
    </div>          
      <div class="visualization-grid"> 
      <div class="score-section">
        <MetaScoreDistribution :gameData="filteredGameData" />
        <UserScoreDistribution :gameData="filteredGameData" />
        <MetaReviewRatio :gameData="filteredGameData" />
        <UserReviewRatio :gameData="filteredGameData" />
      </div>
        <h2 class="section-title">开发商数据分析</h2>
        <div class="developer-section">          
          <DeveloperPublisherStats :gameData="gameData" />
          <DeveloperScoreStability :gameData="gameData" /> 
        </div>
    </div>
      <h2 class="section-title">发行商数据分析</h2>    

      <div class="publisher-filter">
        <span style="color: #fff;">筛选发行商：</span>
        <button
          v-for="publisher in topPublishers"
          :key="publisher"
          :class="{ active: selectedPublisher.includes(publisher) }"
          @click="
            selectedPublisher = selectedPublisher.includes(publisher)
              ? selectedPublisher.filter(p => p !== publisher)
              : [...selectedPublisher, publisher]
          "
        >{{ publisher }}</button>
        <button
          :class="{ active: !selectedPublisher.length }"
          @click="selectedPublisher = []"
        >全部</button>
      </div>
      <div class="visualization-grid">
      <ReleaseTrend :gameData="filteredPublisherData" /> 
      <GameTypeDistribution :gameData="filteredPublisherData" />
    </div>
  </div>
</template>

<style scoped>
.visualization-page {
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  left: 100px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #fff4f4;
  font-size: 2.2rem;
}

h2.section-title {
  grid-column: 1 / -1;
  margin: 30px 0 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #eee;
  color: #fef2f2;
  font-size: 1.6rem;
}

.type-filter {
  margin-bottom: 30px;
  text-align: center;
}
.type-filter button {
  margin: 0 8px 8px;
  padding: 8px 18px;
  border: 1px solid #ddd;
  background: #f5f5f5;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.95rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.type-filter button:hover {
  background: #e9e9e9;
}
.type-filter button.active,
.publisher-filter button.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.publisher-filter {
  margin-bottom: 30px;
  text-align: center;
}
.publisher-filter button {
  margin: 0 8px 8px;
  padding: 8px 18px;
  border: 1px solid #ddd;
  background: #f5f5f5;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.95rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.publisher-filter button:hover {
  background: #e9e9e9;
}

.visualization-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

.score-section,
.analysis-section {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

.score-section {
  background: rgba(64, 158, 255, 0.03);
  padding: 20px;
  border-radius: 12px;
}

.analysis-section {
  background: rgba(103, 194, 58, 0.03);
  padding: 20px;
  border-radius: 12px;
}

.developer-section {
  grid-column: 1 / -1; /* 占据整个网格宽度 */
  display: grid;
  grid-template-columns: 1fr; /* 子元素上下排列 */
  gap: 30px;
}
.developer-section > div {
  width: 100% !important;
  min-width: 0; /* 防止宽度被最小宽度限制 */
}

/* 如果使用了特定组件类名，也可以针对性调整 */
.DeveloperPublisherStats,
.DeveloperScoreStability {
  width: 100% !important;
  min-width: 0;
}

@media (max-width: 1200px) {
  .visualization-grid,
  .score-section,
  .analysis-section {
    grid-template-columns: 1fr;
  }
}
</style>
