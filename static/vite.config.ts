import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // AutoImport({
    //   // include: [
    //   //   // /\.[tj]sx?$/, // .ts, .tsx, .js, .jsx
    //   //   /\.vue$/, /\.vue\?vue/, // .vue
    //   //   // /\.md$/, // .md
    //   // ],
    //   resolvers: [ElementPlusResolver({importStyle: "sass"})],
    // }),
    Components({
      extensions: ['vue', 'md'],
      resolvers: [ElementPlusResolver({importStyle: "sass"})],
      include: [/\.vue$/, /\.vue\?vue/, /\.md$/],
      dts: 'src/components.d.ts',
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
