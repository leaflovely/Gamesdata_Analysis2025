<script setup>
import { ref } from "vue";
import { searchGame } from "../api/game";
import { gameStore } from "../store/game";
import logo from '/src/assets/logo.png';

const inpValue = ref("");
const game = gameStore();

const handleSearch = async () => {
  const res = await searchGame({ question: inpValue.value });
  game.changeGameData(res);
};
</script>

<template>
  <div class="modern-search">
    <div class="search-logo">
      <img
        :src="logo"
        alt="logo"
        style="width: 48px; height: 48px; border-radius: 50%">
      <span class="logo-text">专业的游戏评分网站</span>
    </div>
    <div class="search-group">
      <el-input
        v-model="inpValue"
        style="border: none; width: 400px; height: 40px"
        placeholder="请输入搜索内容"
        @keyup.enter="handleSearch"
        clearable
        class="modern-input"
      >
        <template #append>
          <button class="modern-search-btn" @click="handleSearch">
            <el-icon>
              <search />
            </el-icon>
            <span></span>
          </button>
        </template>
      </el-input>
    </div>
  </div>
</template>


<style lang="less" scoped>
.modern-search {
  width: 97%;
  display: flex;
  align-items: center;
  background: linear-gradient(150deg, #1d529c 0%, #0c3a98 100%); // 渐变色
  border-radius: 12px;
  padding: 0 16px;
  min-height: 60px;
  box-shadow:
    0 8px 32px 0 rgba(8, 22, 65, 0.28),  /* 主阴影，模糊更大更深 */
    0 1.5px 6px 0 rgba(0,0,0,0.12);      /* 轻微叠加柔化 */
}

.search-logo {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-right: 12px;
}
.logo-text {
  margin-left: 10px; // 图片和文字间距
  font-size: 22px;
  font-weight: bold;
  letter-spacing: 2px;
  white-space: nowrap;
  background: linear-gradient(90deg, #7a5fff 0%, #057ce7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

.search-group {
  margin-left: auto;
  display: flex;
  align-items: center;
}

.modern-input {
  ::v-deep(.el-input__wrapper) {
    background: #123464;
    border-radius: 8px 0 0 8px;
    color: #fff;
    font-size: 14px;
    border: 2px solid #057ee7d1;
    border-right: none;
    box-shadow: none;
    transition: border 0.3s;
    height: 35px;
  }
  ::v-deep(.el-input__inner) {
    background: #123464;
    color: #cfcfe1;
    &::placeholder {
      color: #b3b3cc;
      opacity: 0.8;
    }
    height: 30px;
    line-height: 30px;
  }
  ::v-deep(.el-input-group__append) {
    padding: 0;
    background: #081641;
    border: none;
    border-radius: 0 20px 20px 0;
    height: 40px;
  }
}

.modern-search-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 16px;
  border: none;
  border-radius: 0 8px 8px 0;
  background: linear-gradient(90deg, #6751d8 0%, #057ce7 100%);
  color: #fff;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
  box-shadow: none;
  border: 2px solid #057ee78a;
  border-left: none;
  &:hover {
    background: linear-gradient(90deg, #b3b3cc 0%, #2360b3 100%);
    color: #081641;
  }
  span {
    margin-left: 6px;
  }
}
</style>