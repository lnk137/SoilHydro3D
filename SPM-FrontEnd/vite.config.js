import { fileURLToPath, URL } from 'node:url'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    AutoImport({ imports: ['vue','vue-router'],}),
    Components({
      // 配置需要自动注册的组件
      dts: true,
      resolvers: [
        (name) => {
          if (name.startsWith('Base')) {
            return { importName: name.slice(4), path: `@/components/${name}.vue` }
          }
        },
      ],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
