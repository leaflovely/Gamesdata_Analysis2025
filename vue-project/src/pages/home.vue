<script setup>
import Header from "../components/Header.vue";
import Search from "../components/Search.vue";
import HomeNavigation from "../components/HomeNavigation.vue";
import ArticleList from "../components/ArticleList.vue";
import OtherList from "../components/OtherList.vue";
import { ref } from "vue";

const activeName = ref("second");
const tab_list = [
  { name: "first", label: "关注", comp: OtherList },
  { name: "second", label: "推荐", comp: ArticleList },
  { name: "third", label: "资讯", comp: OtherList },
  { name: "fourth", label: "热榜", comp: OtherList },
  { name: "fifth", label: "自荐", comp: OtherList },
  { name: "sixth", label: "动态", comp: OtherList },
];
</script>

<template>
  <!-- 首页内容 -->
  <Header />
  <main>
    <div class="main-box">
      <img src="https://front.cdn.xdclass.net/images/logo.webp" class="logo" />
      <!-- 搜索框 -->
      <div class="search-box">
        <Search />
      </div>
      <!-- 分类导航 -->
      <div style="margin-bottom: 30px">
        <HomeNavigation />
      </div>
      <!-- 文章列表 -->
      <el-tabs v-model="activeName" class="demo-tabs">
        <el-tab-pane
          v-for="item in tab_list"
          :key="item.name"
          :label="item.label"
          :name="item.name"
        >
          <component :is="item.comp" :title="item.label" />
        </el-tab-pane>
      </el-tabs>
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
