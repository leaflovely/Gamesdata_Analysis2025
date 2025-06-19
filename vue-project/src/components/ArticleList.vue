<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { getArticle } from "../api/article";
import { articleStore } from "../store/article";

const router = useRouter();
const article = articleStore();

// 获取文章接口逻辑
const getArticleData = async () => {
  const res = await getArticle();
  article.changeArticleData(res);
};

// 获取文章接口调用
onMounted(() => {
  getArticleData();
});

// 跳转详情页
const goDetail = (data) => {
  router.push({
    path: "/detail",
    query: { data: JSON.stringify(data) },
  });
};
</script>

<template>
  <ul>
    <li
      v-for="item in article.articleData"
      :key="item.id"
      @click="goDetail(item)"
    >
      <h3>{{ item.question }}</h3>
      <div v-html="item.answer"></div>
      <div>
        <span
          ><el-icon><CaretTop /></el-icon> {{ item.up }}赞
        </span>
        <span
          ><el-icon><CaretBottom /></el-icon> {{ item.down }}踩
        </span>
        <span>作者: {{ item.author }}</span>
      </div>
    </li>
  </ul>
</template>

<style lang="less" scoped>
ul {
  width: 100%;
  height: auto;
  overflow: hidden;
  box-sizing: border-box;
  list-style: none;
  margin: 0;
  padding: 0;
  li {
    border-bottom: 2px solid #ccc;
    padding: 10px;
    transition: 0.3s ease;
    list-style: none;
    margin: 0;
    padding: 0;
    h3,
    p {
      margin-bottom: 10px;
    }
    h3 {
      font-size: 18px;
      color: #222226;
    }
    p {
      font-size: 14px;
      font-size: #555666;
    }
    div {
      span {
        margin-right: 24px;
        font-size: 14px;
        font-size: #555666;
      }
    }
    &:hover {
      background: #eeefef;
    }
  }
}
</style>
