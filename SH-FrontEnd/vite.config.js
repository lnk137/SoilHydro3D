import { fileURLToPath, URL } from 'node:url'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: "0.0.0.0", // 监听所有网络接口
    port: 5173,      // 可选，指定开发服务器端口
  },
  plugins: [
    vue(),
    // vueDevTools(),
    AutoImport({ imports: ['vue','vue-router'],resolvers: [ElementPlusResolver()],}),
    Components({
      // 配置需要自动注册的组件
      dts: true,
      resolvers: [
        (name) => {
          if (name.startsWith('Base')) {
            return { importName: name.slice(4), path: `@/components/${name}.vue` }
          }
        },ElementPlusResolver(),
      ],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
