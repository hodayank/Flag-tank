import {defineConfig} from 'vite';export default defineConfig({base:'./',build:{assetsDir:'scripts',rollupOptions:{input:{game:'index.html',viewer:'viewer.html'}}}});
