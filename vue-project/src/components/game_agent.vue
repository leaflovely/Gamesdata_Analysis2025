<template>
    <div ref="cozeContainer"></div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  // 容器引用
  const cozeContainer = ref(null);
  
  onMounted(() => {
    // 确保SDK脚本已加载
    const loadScript = (src) => {
      return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    };
  
    // 加载Coze SDK
    loadScript('https://lf-cdn.coze.cn/obj/unpkg/flow-platform/chat-app-sdk/1.2.0-beta.10/libs/cn/index.js')
      .then(() => {
        // 初始化SDK
        const cozeWebSDK = new CozeWebSDK.WebChatClient({
          config: {
            bot_id: '7520143597971816500',
          },
          componentProps: {
            title: 'Coze',
          },
          auth: {
            type: 'token',
            token: 'pat_DsElm4hqkseLYOT42eH4DmxOfBKiKMEU0XQV4N440BMOIpwqDIRIe3xCuKqiTodS',
            onRefreshToken: function () {
              return 'pat_DsElm4hqkseLYOT42eH4DmxOfBKiKMEU0XQV4N440BMOIpwqDIRIe3xCuKqiTodS';
            },
          },
          ui: {
            header: {
              isShow: false,
            },
            footer: {
              expressionText: '你可以随意问我游戏有关的问题哦！',
            },
            chatBot: {
              isNeedFunctionCallMessage:false,
            }
          }
        });
  
        // 将聊天组件挂载到容器
        cozeWebSDK.mount(cozeContainer.value);
      })
      .catch((error) => {
        console.error('加载Coze SDK失败:', error);
      });
  });
  </script>
  
  <style scoped>
  /* 可以在这里添加自定义样式 */
  </style>    