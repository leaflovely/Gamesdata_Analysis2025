<template>
  <div class="star-rating">
    <h3>请您评分</h3>
    <div class="rating-container">
      <span
        v-for="(star, index) in 10"
        :key="index"
        :class="{ 
          'star': true, 
          'star-filled': index < (hoverRating || selectedRating),
          'star-existing': index < existingRating
        }"
        @mouseover="hoverRating = index + 1"
        @mouseleave="hoverRating = 0"
        @click="selectRating(index + 1)"
      >★</span>
    </div>
    <div class="rating-info">
      <span class="rating-value">{{ selectedRating || existingRating || 0 }}/10</span>
      <el-button 
        type="primary" 
        @click="confirmRating"
        :disabled="selectedRating === 0"
      >确认评分</el-button>
    </div>
    
    <!-- 登录提示弹窗 -->
    <el-dialog
      v-model="showLoginPrompt"
      title="请登录"
      width="400"
      :show-close="false"
      :close-on-click-modal="false"
    >
      <div class="login-prompt">
        <p>您需要登录后才能进行评分！</p>
        <div class="actions">
          <el-button @click="showLoginPrompt = false">取消</el-button>
          <el-button type="primary" @click="openLoginPopup">立即登录</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { userStore } from '../store/user';
import { popStore } from '../store/pop';
import { sendRating } from '../api/user';

const props = defineProps({
  gameId: {
    type: Number,
    required: true
  },
  existingRating: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['rating-submitted']);

const user = userStore();
const pop = popStore();
const selectedRating = ref(0);
const hoverRating = ref(0);
const existingRating = ref(0);
const showLoginPrompt = ref(false);

// 初始化显示已有评分
onMounted(() => {
  if (props.existingRating > 0) {
    selectedRating.value = props.existingRating;
    existingRating.value = props.existingRating;
  }
});

// 监听existingRating变化
watch(() => props.existingRating, (newVal) => {
  if (newVal > 0) {
    selectedRating.value = newVal;
    existingRating.value = newVal;
  }
});

const selectRating = (newRating) => {
  selectedRating.value = newRating;
};

const openLoginPopup = () => {
  showLoginPrompt.value = false;
  pop.changeLoginPop(true);
};

const confirmRating = async () => {
  if (!user.isLogin) {
    showLoginPrompt.value = true;
    return;
  }
  
  if (selectedRating.value === 0) {
    ElMessage.warning('请选择评分');
    return;
  }
  
  try {
    const data = {
      username: user.username,
      rating: selectedRating.value,
      gameId: props.gameId
    };
    await sendRating(data);
    
    // 显示评分成功提示
    ElMessage.success({
      message: '评分成功！',
      duration: 1 // 1.5秒后自动关闭
    });
    
    // 更新现有评分
    existingRating.value = selectedRating.value;
    
    // 通知父组件评分已提交
    emit('rating-submitted', selectedRating.value);
    
    // 1.5秒后刷新页面
    setTimeout(() => {
      window.location.reload(); // 自动刷新页面
    }, 1);
    
  } catch (error) {
    console.error('评分失败:', error);
    ElMessage.error(`评分失败: ${error.message || '请稍后再试'}`);
  }
};
</script>

<style scoped>
.star-rating {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.rating-container {
  display: flex;
  margin: 15px 0;
}

.star {
  font-size: 28px;
  color: #ccc;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-right: 5px;
}

.star:hover {
  color: #ffc107;
  text-shadow: 0 0 8px rgba(255, 193, 7, 0.7);
}

.star-filled {
  color: #ffc107;
  text-shadow: 0 0 8px rgba(255, 193, 7, 0.7);
}

.star-existing {
  color: #ffc107;
}

.rating-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.rating-value {
  font-size: 18px;
  font-weight: bold;
  color: #ffc107;
}

/* 登录提示样式 */
.login-prompt {
  text-align: center;
  padding: 20px;
}

.login-prompt p {
  font-size: 16px;
  margin-bottom: 20px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}
</style>