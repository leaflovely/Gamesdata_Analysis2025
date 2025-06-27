import { defineStore } from "pinia";
import { filterGames } from "../api/game";

export const gameStore = defineStore("game", {
  state: () => ({
    gameData: [],
  }),
  
  actions: {
    changeGameData(data) {
      this.gameData = data;
    },
    
    // 添加筛选方法
    async filterGames(filters) {
      try {
        const res = await filterGames(filters);
        // 需要从response中获取data字段
        this.changeGameData(res.data); 
        return res.data;
      } catch (error) {
        console.error("筛选游戏失败:", error);
        return [];
      }
    },
  },
});
