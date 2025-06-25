<template>
  <div class="game-carousel-container">
    <!-- 轮播区域 -->
    <div class="carousel-wrapper" @mouseenter="pauseAutoPlay" @mouseleave="startAutoPlay">
      <div class="carousel-track" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
        <div 
          v-for="(game, index) in games" 
          :key="index" 
          class="carousel-item"
          @click="showDetail(game)"
        >
          <div class="image-container">
            <img 
              :src="getImagePath(game.image)" 
              :alt="game.chinese_name"
              loading="lazy"
              class="carousel-image"
            >
            <div class="image-overlay">
              <h3 class="game-title">{{ game.chinese_name }}</h3>
              <p class="game-meta">  {{ game.platform }}<br>{{ game.release_date }}</p>
            </div>
          </div>
        </div>
      </div>
      <!-- 左右滑动按钮 -->
      <button class="carousel-control prev" @click="prevSlide" aria-label="上一张">
        <span>&lt;</span>
      </button>
      <button class="carousel-control next" @click="nextSlide" aria-label="下一张">
        <span>&gt;</span>
      </button>
      
      <!-- 指示器 -->
      <div class="carousel-indicators">
        <span 
          v-for="(_, idx) in games" 
          :key="idx"
          :class="{ active: currentIndex === idx }"
          @click="currentIndex = idx"
        ></span>
      </div>
    </div>
    
    <!-- 详情弹窗 -->
    <div v-if="activeGame" class="detail-modal" @click.self="closeDetail">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">{{ activeGame.chinese_name }}</h2>
          <button class="close-button" @click="closeDetail">
            <i class="fa fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="game-hero">
            <img 
              :src="getImagePath(activeGame.image)" 
              :alt="activeGame.chinese_name"
              class="hero-image"
            >
            <div class="game-meta">
              <div class="meta-item">
                <span class="meta-label">发布日期:</span>
                <span class="meta-value">{{ activeGame.release_date }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">平台:</span>
                <span class="meta-value">{{ activeGame.platform }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">Meta评分:</span>
                <span class="meta-value score">{{ activeGame.meta_score }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">玩家评分:</span>
                <span class="meta-value score">{{ activeGame.user_score }}</span>
              </div>
            </div>
          </div>
          
          <div class="game-description">
            <h3>游戏介绍</h3>
            <p>{{ activeGame.information }}</p>
          </div>
          
          <div class="game-reviews">
            <h3>评价统计</h3>
            <div class="review-stats">
              <div class="review-item">
                <div class="review-label">媒体评价</div>
                <div class="review-value positive">{{ activeGame.meta_positive }} 好评</div>
              </div>
              <div class="review-item">
                <div class="review-label">玩家评分</div>
                <div class="review-value">
                  {{ activeGame.user_positive }} 好评
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

// 游戏数据
const games = ref([
  {
    image: "Stardew Valley.png",
    chinese_name: "星露谷物语",
    name: "Stardew Valley",
    platform: "PC/PS4/Xbox/Switch/iOS",
    release_date: "2016-02-26",
    meta_score: 89,
    meta_positive: "97%",
    user_score: 8.8,
    user_positive: "88%",
    information: "星露谷物语是一款角色扮演风格的农场游戏。你可以选择自己的道路... 你会投入时间种植作物和照顾动物吗？你会在当地村庄花时间，与当地村民交朋友吗？你享受在神秘的山洞中屠杀可怕的怪物吗？或者你会尝试完成所有事情，并赢得备受推崇的星露英雄称号？"
  },
  {
    image: "Grand Theft Auto IV.png",
    chinese_name: "侠盗猎车手IV",
    name: "Grand Theft Auto IV",
    platform: "PlayStation 3/Xbox 360/PC",
    release_date: "2008-04-29",
    meta_score: 98,
    meta_positive: "100%",
    user_score: 8.3,
    user_positive: "79%",
    information: "美国梦在今天意味着什么？对于刚从欧洲来的尼科·贝利来说，它是他能够逃避过去的希望。对于他的表哥罗曼来说，它是一个愿景，他们一起可以在自由城找到财富，自由城是通往机会之地的门户。当他们陷入债务并被一系列骗子、小偷和社会病态者拖入犯罪地下场所时，他们发现现实与这个崇拜金钱和地位的城市中的梦想非常不同，对于拥有它们的人来说是天堂，对于没有它们的人来说是噩梦。"
  },
  {
    image: "Granblue Fantasy.png",
    chinese_name: "碧蓝幻想：Relink",
    name: "Granblue Fantasy: Relink",
    platform: "PlayStation 5/PC",
    release_date: "2024-02-01",
    meta_score: 80,
    meta_positive: "84%",
    user_score: 8.3,
    user_positive: "79%",
    information: "“在这个广阔的蓝色世界中，总有更多要探索！让我来展示给你看！”旅程从你的智能手机继续到你的PlayStation 4。来自原碧蓝幻想的艺术家CyDesignation的迷人角色设计和美丽环境，通过PlatinumGames以3D方式生动呈现。PlatinumGames和Cygames合作，将讲述一个以碧蓝幻想中喜爱的角色为主角的新故事，定能让碧蓝和动作游戏爱好者们欣喜不已。"
  },
  {
    image: "Aokana - Four Rhythms Across the Blue.png",
    chinese_name: "苍之彼方的四重奏",
    name: "Aokana - Four Rhythms Across the Blue",
    platform: "Nintendo Switch",
    release_date: "2020-08-21",
    meta_score: 78,
    meta_positive: "63%",
    user_score: 8.2,
    user_positive: "83%",
    information: "在一个骑自行车一样简单就能飞行的世界里，飞行马戏团运动正风靡一时。随着反重力子的发现，允许个人飞行的特殊鞋子——反重力鞋，风靡全球。"
  },
  {
    image: "Baldur's Gate 3.png",
    chinese_name: "博德之门3",
    name: "Baldur's Gate 3",
    platform: "PC/PlayStation 5/Xbox Series X",
    release_date: "2023-08-03",
    meta_score: 96,
    meta_positive: "99%",
    user_score: 9.2,
    user_positive: "90%",
    information: "远古邪恶已回归博德之门，意图从内部吞噬它。费伦的命运掌握在你手中。独自一人，你可以抵抗。但一起，你可以战胜。召集你的队伍，回到被遗忘的国度，在一段关于友谊与背叛、牺牲与生存以及绝对力量的诱惑的故事中。神秘的能力在你体内觉醒，来自植入你大脑的食脑魔寄生虫。抵抗，让黑暗自我毁灭。或者拥抱腐败，成为终极邪恶。"
  },
  {
    image: "Hollow Knight.png",
    chinese_name: "空洞骑士",
    name: "Hollow Knight",
    platform: "PC/Nintendo Switch/Xbox One",
    release_date: "2018-06-12",
    meta_score: 90,
    meta_positive: "100%",
    user_score: 9.1,
    user_positive: "90%",
    information: "Hollow Knight是一款以传统2D动画和熟练游戏玩法为重点的2D动作冒险游戏。前往Hallownest，一个广阔而古老的地下王国，那里居住着各种奇怪的昆虫和怪物。玩家将他们自己的道路，探索废墟城市、真菌森林、骨庙和其他奇幻土地，所有这些都在他们揭开古代谜团的道路上。"
  }
])

const currentIndex = ref(0)
const activeGame = ref(null)
let autoPlayTimer = null
const isDetailOpen = ref(false) // 新增状态标记详情页是否打开

// 图片路径生成
const getImagePath = (filename) => {
  return `/images/${filename}`
}

// 自动播放逻辑 - 优化定时器管理
const startAutoPlay = () => {
  if (isDetailOpen.value) return // 详情页打开时不启动自动播放
  
  // 先清除可能存在的旧定时器
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer)
  }
  
  // 设置新的定时器
  autoPlayTimer = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % games.value.length
  }, 3000)
}

const pauseAutoPlay = () => {
  clearInterval(autoPlayTimer)
}

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % games.value.length
}

const prevSlide = () => {
  currentIndex.value = (currentIndex.value - 1 + games.value.length) % games.value.length
}

const showDetail = (game) => {
  activeGame.value = game
  pauseAutoPlay()
  isDetailOpen.value = true // 标记详情页已打开
}

const closeDetail = () => {
  activeGame.value = null
  startAutoPlay() // 关闭详情页时启动自动播放
  isDetailOpen.value = false // 标记详情页已关闭
}

onMounted(() => {
  startAutoPlay()
})

onBeforeUnmount(() => {
  pauseAutoPlay()
})

// 优化监听逻辑，使用新的状态标记控制自动播放
watch(isDetailOpen, (newVal) => {
  if (newVal) {
    pauseAutoPlay()
  } else {
    startAutoPlay()
  }
})
</script>

<style scoped>
/* 轮播容器 */
.game-carousel-container {
  position: relative;
  max-width: 1200px;
  margin: 40px auto;
}

.carousel-control {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  color: #ffffff6a;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  font-size: 2rem;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.5;
  transition: background 0.2s, opacity 0.2s;
  user-select: none;
}
.carousel-control:hover {
  background: rgba(0,0,0,0.2);
  opacity: 1;
}
.carousel-control.prev {
  left: 16px;
}
.carousel-control.next {
  right: 16px;
}

.carousel-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.carousel-track {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.carousel-item {
  min-width: 100%;
  position: relative;
}

.image-container {
  position: relative;
  height: 0;
  padding-top: 56.25%; /* 16:9 比例 */
  background: #f5f5f5;
}

.carousel-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.carousel-item:hover .carousel-image {
  transform: scale(1.02);
}

.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0));
  padding: 20px 30px;
  color: white;
  transform: translateY(20px);
  opacity: 0;
  transition: all 0.3s ease;
}

.carousel-item:hover .image-overlay {
  transform: translateY(0);
  opacity: 1;
}

.game-title {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.game-meta {
  margin: 0;
  font-size: 1rem;
  color: #e0e0e0;
}

/* 控制按钮 */
.carousel-control {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  opacity: 0;
  transition: all 0.3s;
}

.carousel-wrapper:hover .carousel-control {
  opacity: 1;
}

.carousel-control:hover {
  background: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(-50%) scale(1.05);
}

.prev {
  left: 20px;
}

.next {
  right: 20px;
}

/* 指示器 */
.carousel-indicators {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 10;
}

.carousel-indicators span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s;
}

.carousel-indicators span.active {
  background: #3b82f6;
  width: 30px;
  border-radius: 6px;
}

/* 内容预留区域 */
.content-placeholder {
  min-height: 200px;
  margin-top: 30px;
  border: 2px dashed #e0e0e0;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
  font-size: 18px;
  color: #666;
}

/* 详情弹窗 */
.detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  backdrop-filter: blur(5px);
  animation: fadeIn 0.3s ease forwards;
}

.modal-content {
  width: 90%;
  max-width: 900px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  animation: scaleIn 0.3s ease forwards;
}

.modal-header {
  padding: 20px 30px;
  background: #1e40af;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: transform 0.3s;
}

.close-button:hover {
  transform: rotate(90deg);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
}

.game-hero {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.hero-image {
  width: 300px;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.game-meta {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.meta-item {
  background: #f3f4f6;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow:
    0 8px 32px rgba(143, 143, 143, 0.18),   /* 蓝色主阴影更大更深 */
    0 2px 8px rgba(0,0,0,0.08);
}

.meta-label {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 5px;
}

.meta-value {
  color: #3e3e3e;
  font-size: 1.1rem;
  font-weight: 500;
}

.score {
  color: #10b981;
  font-weight: 600;
}

.game-description,
.game-reviews {
  margin-bottom: 30px;
}

.game-description h3,
.game-reviews h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #1f2937;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 10px;
}

.game-description p {
  line-height: 1.8;
  color: #4b5563;
}

.review-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 50px;
}

.review-item {
  background: #f9fafb;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #3b82f6;
  box-shadow:
    0 8px 32px rgba(59, 130, 246, 0.18),   /* 蓝色主阴影更大更深 */
    0 2px 8px rgba(0,0,0,0.08);
}

.review-label {
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 8px;
}

.review-value {
  color: #10b981;
  font-size: 1.2rem;
  font-weight: 500;
}

.positive {
  color: #10b981;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.95); }
  to { transform: scale(1); }
}
</style>
