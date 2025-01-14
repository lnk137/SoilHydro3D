import { createRouter, createWebHashHistory } from "vue-router";


const router = createRouter({
  history: createWebHashHistory(), // 使用 Hash 模式的路由历史记录
  routes: [
    // { path: "/", redirect: "/Import" }, 
    // { path: "/import", component: Import, name: "import" },
    // { path: "/paint", component: Paint, name: "paint" },
    // { path: "/model", component: Model, name: "model" },
    // { path: "/camera", component: Camera ,name: "camera" },
    // { path: "/test", component: Test ,name: "test" },
  ],
});

export default router;
