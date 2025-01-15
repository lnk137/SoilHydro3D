import { createRouter, createWebHashHistory } from "vue-router";
import set from "@/views/set.vue";
import test from "@/views/test.vue";

const router = createRouter({
  history: createWebHashHistory(), // 使用 Hash 模式的路由历史记录
  routes: [
    { path: "/", redirect: "/set" }, 
    { path: "/set", component: set, name: "set" },
    { path: "/test", component: test, name: "test" },
    // { path: "/model", component: Model, name: "model" },
    // { path: "/camera", component: Camera ,name: "camera" },
    // { path: "/test", component: Test ,name: "test" },
  ],
});

export default router;
