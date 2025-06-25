<script setup>
import Header from "../components/Header.vue";
import Search from "../components/Search.vue";
//import ExploreLite from "../components/ExploreLite.vue"; 
import GameList from "../components/Game.vue";
import OtherList from "../components/OtherList.vue";
import { ref } from "vue";
import CarouselWithDetail from '../components/CarouselWithDetail.vue'
  
const activeName = ref("second");
</script>

<template>
  <!-- 首页内容 -->
  <Header />
  <div class="custom-gap"></div> 
  <main>
    <div class="main-box">
      <Search />
      <div class="carousel-tip">
        游戏推荐 ———来自我们编辑的精选游戏
      </div>
      <CarouselWithDetail />

      <!-- 其它组件 -->
    </div>
  </main>
</template>


<style lang="less">
body {
  min-height: 100vh;
  background: linear-gradient(150deg, #0b508d 0%, #081641 100%);
  /* 你可以根据需要调整渐变角度和颜色 */
}
</style>

<style lang="less" scoped>
.custom-gap {
  height: 32px;
  background:transparent;
}
main {
  background-color: transparent;
  overflow: hidden;

  .main-box {
    width: 1200px;
    margin: 0 auto;
    margin-left: 400px; // 新增，向右平移80px
  }
  .carousel-tip {
    color: #fff;
    font-size: 40px;
    margin-top: 20px;
    margin-bottom: 0 auto;
    text-align: left;
    letter-spacing: 1px;
    font-weight: 500;
  }
  .section-title {
    color: #fff;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 20px;
    margin-top: 20px;
    letter-spacing: 2px;
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
