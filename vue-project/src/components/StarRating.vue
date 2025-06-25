<template>
    <div class="star-rating">
      <div class="stars">
        <span 
          v-for="index in 10" 
          :key="index"
          class="star"
          :class="{
            'filled': (hoverRating >= index) || (!hoverRating && selectedRating >= index)
          }"
          @mouseover="hoverRating = index"
          @mouseleave="hoverRating = 0"
          @click="selectRating(index)"
        >
          ★
        </span>
      </div>
      <el-button 
        type="primary" 
        @click="submitRating"
        :disabled="selectedRating === 0"
      >
        确认评分
      </el-button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { userStore } from '../store/user';
  import { popStore } from '../store/pop';
  import { rateGame } from '../api/game';
  
  const user = userStore();
  const pop = popStore();
  
  const props = defineProps({
    gameId: Number
  });
  
  const selectedRating = ref(0);
  const hoverRating = ref(0);
  
  const selectRating = (rating) => {
    selectedRating.value = rating;
  };
  
  const submitRating = () => {
    if (!user.isLogin) {
      pop.changeLoginPop(true);
      return;
    }
    
    // 调用评分API
    rateGame({
      gameId: props.gameId,
      rating: selectedRating.value,
      userId: user.userId
    }).then(() => {
      ElMessage.success('评分成功');
    }).catch(error => {
      ElMessage.error(`评分失败: ${error.message}`);
    });
  };
  </script>
  
  <style scoped>
  .star-rating {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
  }
  
  .stars {
    font-size: 28px;
    margin-bottom: 15px;
  }
  
  .star {
    cursor: pointer;
    color: #ccc;
    transition: color 0.2s;
    margin: 0 2px;
  }
  
  .star.filled {
    color: #ffc107; /* 黄色 */
  }
  </style>