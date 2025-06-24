<script setup>
import Header from "../components/Header.vue";
import Search from "../components/Search.vue";
import GameList from "../components/Game.vue";
import OtherList from "../components/OtherList.vue";
import { ref } from "vue";

const activeName = ref("second");
</script>

<template>
  <!-- 首页内容 -->
  <Header />
  <main>
    <div class="main-box">
      
      <div class="search-box">
        <Search />
      </div>
    </div>
  </main>
</template>

<style lang="less" scoped>
main {
  background-color: hsla(0, 0%, 98%, 0.8);
  overflow: hidden;

  .main-box {
    width: 1200px;
    margin: 0 auto;
  }
  .logo {
    display: block;
    width: 213px;
    height: 100px;
    margin: 0 auto;
  }
  .search-box {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }

  .demo-tabs > .el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
  }
}
</style>
