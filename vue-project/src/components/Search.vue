<script setup>
import { ref } from "vue";
import { searchGame } from "../api/game";
import { gameStore } from "../store/game";

const inpValue = ref("");
const game = gameStore();

// 搜索游戏
const handleSearch = async () => {
  const res = await searchGame({ question: inpValue.value });
  game.changeGameData(res);
};
</script>

<template>
  <div>
    <el-input
      v-model="inpValue"
      style="border: 1px solid #ccc; width: 600px; height: 40px"
      placeholder="请输入搜索内容"
    >
      <template #append>
        <button class="search-btn" @click="handleSearch">
          <el-icon>
            <search />
          </el-icon>
          <span>搜索</span>
        </button>
      </template>
    </el-input>
  </div>
</template>

<style lang="less" scoped>
::v-deep(.el-input-group__append) {
  // padding: 0;
  padding: 0;
  width: 88px;
}
::v-deep(.el-input__wrapper) {
  box-shadow: none;
  &.is-focus {
    box-shadow: none;
  }
  &:hover {
    box-shadow: none;
  }
}
.search-btn {
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  background: #fc5531;
  color: white;
  font-size: 16px;
  transition: 0.4s ease;
  span {
    margin-left: 5px;
  }
  &:hover {
    background: #fc1944;
  }
}
</style>