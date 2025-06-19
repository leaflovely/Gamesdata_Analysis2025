<script lang="ts" setup>
import Editor from "../components/Editor.vue";
import Header from "../components/Header.vue";
import { publishArticle } from "../api/article";
import { userStore } from "../store/user";
import router from "../router.js";
import { ref } from "vue";
import { ElMessage } from "element-plus";

const editorData = ref("");
const titleData = ref("");
const user = userStore();

const handlePublish = async () => {
  const res = await publishArticle({
    question: titleData.value,
    answer: editorData.value,
    author: user.username,
    up: "11",
    down: "0",
  });
  if ((res as any) === "发布成功") {
    ElMessage.success({
      message: "发布成功",
      type: "success",
    });
    router.push("/home");
  }
};
</script>

<template>
  <div class="editor-out">
    <Header />
    <div class="editor">
      <div class="title">
        <div class="titl">文章标题</div>
        <el-input v-model="titleData"></el-input>
      </div>
      <div class="editor-com">
        <Editor v-model:content="editorData" />
      </div>
      <div class="publish" @click="handlePublish">
        <el-button class="plus-btn">
          <span>发布</span>
        </el-button>
      </div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.publish {
  margin-top: 50px;
  .plus-btn {
    background-color: #fc5531;
    width: 80px;
    height: 32px;
    color: white;
    margin-left: 16px;
    &:hover {
      color: white;
    }
    border-radius: 14px;
  }
}
.editor-out {
  .editor {
    padding: 50px 0;
    width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-content: center;
    justify-content: center;
    align-items: center;
    .title {
      margin-bottom: 50px;
      display: flex;
      align-items: center;
      width: 500px;
      height: 40px;
      .titl {
        width: 100px;
      }
    }
    .editor-com {
      height: 600px;
    }
  }
}
</style>
