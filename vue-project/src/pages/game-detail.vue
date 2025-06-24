<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import Header from "../components/Header.vue";
import dayjs from "dayjs";

const gameData = ref("");

const { query } = useRoute();
const getGameData = () => {
  gameData.value = JSON.parse(query.data);
};

getGameData();
</script>

<template>
  <div class="big-box">
    <!-- 头部 -->
    <Header />
    <main>
      <h1>{{ gameData.question }}</h1>
      <div class="illustrate">
        <div class="top">
          <span class="first">原创</span>
          <span>作者:{{ gameData.author }}</span>
          <span>
            <el-icon><Clock /></el-icon>
            {{ dayjs(gameData.publish_time).format("YYYY-MM-DD HH:mm:ss") }}
          </span>
          <span>
            <el-icon><ArrowUp /></el-icon>
            点赞数{{ gameData.up }}
          </span>
          <span>
            <el-icon><ArrowDown /></el-icon>
            踩{{ gameData.down }}
          </span>
        </div>
      </div>
      <div class="content">
        <div v-html="gameData.answer" />
      </div>
    </main>
  </div>
</template>

<style lang="less" scoped>
header {
  position: sticky;
  top: 0;
}
.big-box {
  width: 100vw;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: scroll;
}
main {
  background: white;
  width: 1200px;
  height: 100vh;
  margin: 8px auto 0;
  box-shadow: 0 0 2px 2px #eee;
  border-radius: 4px;
  padding: 24px;
  h1 {
    font-size: 24px;
    margin: 10px 0;
  }
  .illustrate {
    height: 72px;
    background: #efefef;
    border-radius: 4px;
    padding: 10px;
    box-sizing: border-box;
    span {
      margin-right: 16px;
      &.first {
        display: inline-block;
        height: 50%;
        width: 40px;
        background: #ff5531;
        color: white;
        text-align: center;
      }
      &.last {
        display: inline-block;
        font-size: 12px;
        float: right;
      }
      font-size: 14px;
      color: #999aaa;
    }
    .bottom {
      margin-top: 10px;
    }
  }
  .content {
    border-left: 8px solid #dddfe4;
    background: #eef0f4;
    padding: 16px;
    margin-top: 20px;
    p {
      font-size: 16px;
      line-height: 24px;
    }
  }
}
</style>
