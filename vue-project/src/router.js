import { createRouter, createWebHashHistory } from "vue-router";
import Home from "./pages/home.vue";
import { ElMessage } from "element-plus";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", component: Home },
  {
    path: '/visualization',
    name: 'Visualization',
    component: () => import('./pages/VisualizationPage.vue')
  },
  {
    path: '/all-games',
    name: 'AllGames',
    component: () => import('./components/AllGames.vue')
  },
  {
    path: '/explore-queue',
    name: 'ExploreQueue',
    component: () => import('./components/ExploreQueue.vue')
  },
  {
    path: '/my-evaluate',
    name: 'MyEvaluate',
    component: () => import('./components/MyEvaluate.vue'),
    meta: { requiresAuth: true } // 需要登录的页面
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// 路由拦截守卫
router.beforeEach((to, from, next) => {
  //判断是否需要登录权限
  if (to.meta.isAuth) {
    if (localStorage.getItem("token")) {
      next();
    } else {
      ElMessage.error({
        message: "请先登录",
        type: "error",
      });
      router.push("/home");
    }
  } else {
    next();
  }
});

export default router;
