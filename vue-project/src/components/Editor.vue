<script lang="ts" setup>
import { QuillEditor } from "@vueup/vue-quill";
import { ref } from "vue";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

const toolbar = ref([
  ["bold", "italic", "underline", "strike"],
  ["image", "blockquote", "code-block"],

  [{ list: "ordered" }, { list: "bullet" }],
  [{ script: "sub" }, { script: "super" }],
  [{ indent: "-1" }, { indent: "+1" }],

  [{ header: [1, 2, 3, 4, 5, 6, false] }],

  ["clean"],
]);
</script>

<template>
  <QuillEditor contentType="html" theme="snow" :toolbar="toolbar" />
</template>
