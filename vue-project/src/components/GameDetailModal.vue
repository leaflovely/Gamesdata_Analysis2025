<template>
  <teleport to="body">
    <transition name="fade">
      <div v-if="visible" class="modal-overlay" @click.self="close">
        <div class="modal-container">
          <!-- 头部区域 -->
          <div class="modal-header">
            <h2 class="game-title">{{ game.chinese_name || game.name }}</h2>
            <p class="game-subtitle">{{ game.name }}</p>
            <button class="close-btn" @click="close">
              <span class="material-icons">close</span>
            </button>
          </div>

          <!-- 主要内容区域 -->
          <div class="modal-content">
            <div class="basic-info">
              <div class="info-item">
                <span class="info-label">平台:</span>
                <span class="info-value">{{ game.platform }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">发行日期:</span>
                <span class="info-value">{{ formatDate(game.release_date) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">开发商:</span>
                <span class="info-value">{{ game.developer }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">发行商:</span>
                <span class="info-value">{{ game.publisher }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">游戏类型:</span>
                <span class="info-value">{{ game.genres }}</span>
              </div>
            </div>

            <!-- 评分区域 -->
            <div class="rating-section">
              <div class="rating-card meta-rating">
                <h3>Meta评分</h3>
                <div class="score-badge">{{ game.meta_score }}</div>
                <div class="review-stats">
                  <div class="stat-item">
                    <span class="stat-label">评论数:</span>
                    <span class="stat-value">{{ game.meta_reviews_number }}</span>
                  </div>
                  <div class="sentiment-bar">
                    <div class="sentiment positive" :style="{ width: game.meta_positive + '%' }">
                      <span>{{ game.meta_positive }}%</span>
                    </div>
                    <div class="sentiment mixed" :style="{ width: game.meta_mixed + '%' }">
                      <span>{{ game.meta_mixed }}%</span>
                    </div>
                    <div class="sentiment negative" :style="{ width: game.meta_negative + '%' }">
                      <span>{{ game.meta_negative }}%</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="rating-card user-rating">
                <h3>用户评分</h3>
                <div class="score-badge">{{ game.user_score.toFixed(1) }}</div>
                <div class="review-stats">
                  <div class="stat-item">
                    <span class="stat-label">评论数:</span>
                    <span class="stat-value">{{ game.user_reviews_number }}</span>
                  </div>
                  <div class="sentiment-bar">
                    <div class="sentiment positive" :style="{ width: game.user_positive + '%' }">
                      <span>{{ game.user_positive }}%</span>
                    </div>
                    <div class="sentiment mixed" :style="{ width: game.user_mixed + '%' }">
                      <span>{{ game.user_mixed }}%</span>
                    </div>
                    <div class="sentiment negative" :style="{ width: game.user_negative + '%' }">
                      <span>{{ game.user_negative }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 游戏介绍 -->
            <div class="game-description">
              <h3>游戏简介</h3>
              <p>{{ game.information || '暂无游戏介绍' }}</p>
            </div>
            <!-- 添加评分组件 -->
            <StarRating 
              v-if="game.id" 
              :game-id="game.id" 
              @rating-submitted="handleRatingSubmitted"
            />
          </div>
        </div>
      </div>
    </transition>
  </teleport>

</template>

<script setup>
import { ref } from "vue";
import { formatDate } from "../utils/dateFormatter";
import StarRating from './StarRating.vue';

// 在现有代码中添加处理评分提交的方法
const handleRatingSubmitted = () => {
  // 这里可以添加更新界面或其他操作
  console.log('评分已提交');
};
const props = defineProps({
  game: {
    type: Object,
    required: true,
    default: () => ({})
  },
  visible: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};
</script>

<style scoped>
/* 遮罩层 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

/* 弹窗容器 */
.modal-container {
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  color: #e6e6e6;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 头部样式 */
.modal-header {
  background: rgba(0, 0, 0, 0.4);
  padding: 20px;
  position: relative;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.game-title {
  font-size: 2rem;
  margin: 0 0 5px 0;
  color: #fff;
  font-weight: 700;
}

.game-subtitle {
  font-size: 1.1rem;
  margin: 0;
  color: #a9a9a9;
  font-style: italic;
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

/* 内容区域 */
.modal-content {
  padding: 20px;
  overflow-y: auto;
  flex-grow: 1;
}

/* 基础信息 */
.basic-info {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.info-item {
  display: flex;
  margin-bottom: 10px;
}

.info-label {
  font-weight: 600;
  color: #4cc9f0;
  min-width: 90px;
}

.info-value {
  flex: 1;
}

/* 评分区域 */
.rating-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 25px;
}

.rating-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.rating-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.meta-rating::before {
  background: linear-gradient(90deg, #43cbff 0%, #9708cc 100%);
}

.user-rating::before {
  background: linear-gradient(90deg, #f6d365 0%, #fda085 100%);
}

.score-badge {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 15px 0;
  background: rgba(0, 0, 0, 0.3);
  width: 80px;
  height: 80px;
  line-height: 80px;
  border-radius: 50%;
  display: inline-block;
}

.meta-rating .score-badge {
  color: #43cbff;
}

.user-rating .score-badge {
  color: #f6d365;
}

.review-stats {
  margin-top: 15px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.sentiment-bar {
  display: flex;
  height: 30px;
  margin-top: 10px;
  border-radius: 4px;
  overflow: hidden;
}

.sentiment {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 600;
  color: #000;
}

.positive {
  background: linear-gradient(to right, #4ade80, #22c55e);
}

.mixed {
  background: linear-gradient(to right, #fbbf24, #f59e0b);
}

.negative {
  background: linear-gradient(to right, #f87171, #ef4444);
}

/* 游戏介绍 */
.game-description {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
}

.game-description h3 {
  margin-top: 0;
  color: #4cc9f0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 10px;
}

.game-description p {
  line-height: 1.6;
  text-align: justify;
}

/* 动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active .modal-container,
.fade-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.fade-enter-from .modal-container,
.fade-leave-to .modal-container {
  transform: scale(0.95);
}
</style>