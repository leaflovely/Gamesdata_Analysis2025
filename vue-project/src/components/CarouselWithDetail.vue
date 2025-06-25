<template>
    <div class="carousel-container">
      <!-- 轮播区域 -->
      <div class="carousel" @mouseenter="pauseAutoPlay" @mouseleave="startAutoPlay">
        <div class="carousel-track" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
          <div 
            v-for="(game, index) in games" 
            :key="index" 
            class="carousel-item"
            @click="showDetail(game)"
          >
            <div class="image-container">
              <img :src="getImagePath(game.image)" :alt="game.chinese_name">
            </div>
          </div>
        </div>
        <button class="carousel-prev" @click="prevSlide">❮</button>
        <button class="carousel-next" @click="nextSlide">❯</button>
        <div class="carousel-indicators">
          <span 
            v-for="(_, idx) in games" 
            :key="idx"
            :class="{ active: currentIndex === idx }"
            @click="currentIndex = idx"
          ></span>
        </div>
      </div>
      
      <!-- 下方预留区域 -->
      <div class="content-placeholder">
        <slot name="additional-content"></slot>
      </div>
  
      <!-- 详情弹窗 -->
      <div v-if="activeGame" class="detail-modal">
        <div class="modal-content">
          <span class="close" @click="activeGame = null">×</span>
          <h2>{{ activeGame.chinese_name }}</h2>
          <div class="meta-info">
            <span>发布日期: {{ activeGame.release_date }}</span>
            <span>平台: {{ activeGame.platform }}</span>
            <span>Meta评分: {{ activeGame.meta_score }}</span>
          </div>
          <p class="description">{{ activeGame.information }}</p>
          <div class="review-stats">
            <div>媒体评价: {{ activeGame.meta_positive }} 好评</div>
            <div>玩家评分: {{ activeGame.user_score }} ({{ activeGame.user_positive }} 好评)</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  
  // 图片文件名与public/images完全匹配
  const games = ref([
    {
      image: "Stardew Valley.png",
      chinese_name: "星露谷物语",
      name: "Stardew Valley",
      platform: "PC/PS4/Xbox/Switch/iOS",
      release_date: "2016-02-26",
      meta_score: 89,
      meta_positive: "97%",
      user_score: "8.8",
      user_positive: "88%",
      information: "星露谷物语是一款RPG风格的农场模拟游戏。你可以选择种田、照顾动物、结交村民、探索矿洞或者成为星露谷英雄。"
    },
    {
      image: "Grand Theft Auto IV.png",
      chinese_name: "侠盗猎车手IV",
      name: "Grand Theft Auto IV",
      platform: "PlayStation 3/Xbox 360/PC",
      release_date: "2008-04-29",
      meta_score: 98,
      meta_positive: "100%",
      user_score: "8.3",
      user_positive: "79%",
      information: "[2008年度最佳游戏] 什么是美国梦？对于刚刚从欧洲来到自由城的Niko Belic来说，是逃离过去的希望，也是和表兄弟Roman在自由城这个充满机遇的土地上追求财富的愿景..."
    },
    {
      image: "Granblue Fantasy.png",
      chinese_name: "碧蓝幻想：Relink",
      name: "Granblue Fantasy: Relink",
      platform: "PlayStation 5/PC",
      release_date: "2024-02-01",
      meta_score: 80,
      meta_positive: "84%",
      user_score: "8.3",
      user_positive: "79%",
      information: "在这个广阔蓝海世界中总有更多值得探索的地方！从手机版到PlayStation 4版的旅程延续，由Cygames和PlatinumGames联手打造的全新故事..."
    },
    {
      image: "Aokana - Four Rhythms Across the Blue.png",
      chinese_name: "苍之彼方的四重奏",
      name: "Aokana - Four Rhythms Across the Blue",
      platform: "Nintendo Switch",
      release_date: "2020-08-21",
      meta_score: 78,
      meta_positive: "63%",
      user_score: "8.2",
      user_positive: "83%",
      information: "在这个天空飞翔如骑自行车般轻松的世界里，飞行马戏团运动大受欢迎。跟随反引力子的发现，特殊飞行鞋让空中漫步成为日常..."
    },
    {
      image: "Baldur's Gate 3.png",
      chinese_name: "博德之门3",
      name: "Baldur's Gate 3",
      platform: "PC/PlayStation 5/Xbox Series X",
      release_date: "2023-08-03",
      meta_score: 96,
      meta_positive: "99%",
      user_score: "9.2",
      user_positive: "90%",
      information: "古老的邪恶已重返博德之门，意图从内部吞噬它。费伦的命运掌握在你手中。独行也许能抵抗，但同心协力才能战胜。聚集你的队伍，回到被遗忘的国度..."
    },
    {
      image: "Hollow Knight.png",
      chinese_name: "空洞骑士",
      name: "Hollow Knight",
      platform: "PC/Nintendo Switch/Xbox One",
      release_date: "2018-06-12",
      meta_score: 90,
      meta_positive: "100%",
      user_score: "9.1",
      user_positive: "90%",
      information: "空洞骑士是一款强调传统2D动画和精湛游戏玩法的2D动作冒险游戏。探索Hallownest，一个由各种昆虫和怪物居住的古老地下王国..."
    }
  ])
  
  const currentIndex = ref(0)
  const activeGame = ref(null)
  let autoPlayTimer = null
  
  // 图片路径生成
  const getImagePath = (filename) => {
    return `/images/${filename}`
  }
  
  // 自动播放逻辑
  const startAutoPlay = () => {
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
  }
  
  onMounted(startAutoPlay)
  onBeforeUnmount(pauseAutoPlay)
  </script>
  
  <style scoped>
  /* 轮播容器 */
  .carousel-container {
    position: relative;
    width: 100%;
    max-width: 1200px;
    margin: 40px auto; /* 上方增加间距避免遮挡 */
  }
  
  .carousel {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }
  
  /* 图片容器 */
  .image-container {
    position: relative;
    height: 0;
    padding-top: 60%; /* 根据图片比例调整 */
    background-color: #f8f8f8;
  }
  
  .carousel-track {
    display: flex;
    transition: transform 0.5s ease;
  }
  
  .carousel-item {
    min-width: 100%;
  }
  
  .carousel-item img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain; /* 确保完整显示图片 */
  }
  
  /* 控制按钮 */
  .carousel-prev, .carousel-next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0,0,0,0.7);
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 24px;
    cursor: pointer;
    z-index: 10;
    opacity: 0.8;
    transition: opacity 0.3s;
  }
  
  .carousel-prev:hover, .carousel-next:hover {
    opacity: 1;
  }
  
  .carousel-prev { left: 20px; }
  .carousel-next { right: 20px; }
  
  /* 指示器 */
  .carousel-indicators {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 12px;
  }
  
  .carousel-indicators span {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: rgba(255,255,255,0.5);
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .carousel-indicators span.active {
    background: #3498db;
    transform: scale(1.2);
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
    background: rgba(0,0,0,0.8);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal-content {
    position: relative;
    width: 90%;
    max-width: 800px;
    max-height: 85vh;
    overflow-y: auto;
    background: #fff;
    border-radius: 12px;
    padding: 40px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
  }
  
  .close {
    position: absolute;
    top: 15px;
    right: 20px;
    font-size: 32px;
    cursor: pointer;
    color: #777;
    transition: color 0.3s;
  }
  
  .close:hover {
    color: #333;
  }
  
  .meta-info {
    display: flex;
    gap: 20px;
    margin: 20px 0;
    font-size: 16px;
    color: #555;
    flex-wrap: wrap;
  }
  
  .meta-info span {
    background: #f0f2f5;
    padding: 6px 12px;
    border-radius: 4px;
  }
  
  .description {
    line-height: 1.8;
    margin: 25px 0;
    color: #333;
    font-size: 16px;
  }
  
  .review-stats {
    display: flex;
    gap: 40px;
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    font-size: 15px;
  }
  
  .review-stats div {
    min-width: 150px;
  }
  </style>