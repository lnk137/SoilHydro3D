<template>
    <div class="window-controls">
      <button @click="toggleFullscreen">⛶</button> <!-- 全屏符号 -->
      <button @click="minimizeWindow">━</button> <!-- 最小化符号 -->
      <button @click="closeWindow">✖</button> <!-- 关闭符号 -->
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import {useUrlStore} from '@/stores/UrlStore';  // 引入 Pinia Store

  const urlStore = useUrlStore();  // 创建 Pinia Store 实例
  // 使用 ref 来存储操作状态
  const isLoading = ref(false);
  
  
  // API 请求函数
  const toggleFullscreen = async () => {
    try {
      isLoading.value = true;
      const response = await fetch(`${urlStore.server_url}/top/fullscreen`, {
        method: 'POST',
      });
      const data = await response.json();
      console.log('切换全屏成功', data);
    } catch (error) {
      console.error('切换全屏失败', error);
    } finally {
      isLoading.value = false;
    }
  };
  
  const minimizeWindow = async () => {
    try {
      isLoading.value = true;
      const response = await fetch(`${urlStore.server_url}/top/minimize`, {
        method: 'POST',
      });
      const data = await response.json();
      console.log('窗口已最小化', data);
    } catch (error) {
      console.error('最小化窗口失败', error);
    } finally {
      isLoading.value = false;
    }
  };
  
  const closeWindow = async () => {
    try {
      isLoading.value = true;
      const response = await fetch(`${urlStore.server_url}/top/close`, {
        method: 'POST',
      });
      const data = await response.json();
      console.log('窗口已关闭', data);
    } catch (error) {
      console.error('关闭窗口失败', error);
    } finally {
      isLoading.value = false;
    }
  };
  </script>
  
  <style scoped>
  .window-controls {
    display: flex;
    justify-content: center;
    gap: 20px;
  }
  
  button {
    margin-bottom: 20px;
    font-size: 24px;
    border: none;
    background-color: transparent;
    cursor: pointer;
    color: #257D6E;
    transition: background-color 0.3s, opacity 0.3s, color 0.3s, scale 0.3s;
  }
  
  button:hover {
    color: #7860e3;
    scale: 1.1;
  }
  </style>
  