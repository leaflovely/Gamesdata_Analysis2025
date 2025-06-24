import { defineStore } from "pinia";
import { ref } from "vue";

export const gameStore = defineStore("game", () => {
  const gameData = ref([]);

  // 改变游戏列表内容
  const changeGameData = (e) => {
    gameData.value = e;
  };

  return {
    gameData,
    changeGameData,
  };
});
