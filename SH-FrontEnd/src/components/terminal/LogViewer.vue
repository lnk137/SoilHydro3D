<script setup>
import { ref, onMounted, watch } from 'vue';

// 定义一个 prop，用于外部传递日志刷新间隔时间（默认为 3000 毫秒）
const props = defineProps({
  refreshInterval: {
    type: Number,
    default: 3000,
  },
});

// 定义日志数据
const logs = ref([]);

// 获取日志的函数
const fetchLogs = async () => {
  try {
    const response = await fetch('http://127.0.0.1:4201/get_logs');
    const data = await response.json();
    logs.value = data; // 更新日志列表
  } catch (error) {
    console.error('获取日志失败', error);
  }
};

// 在组件挂载时执行
onMounted(() => {
  // 尝试从 localStorage 中读取日志数据
  const savedLogs = localStorage.getItem('logs');
  if (savedLogs) {
    logs.value = JSON.parse(savedLogs); // 如果存在，加载到 logs 中
  } else {
    fetchLogs(); // 如果不存在，初次获取日志
  }

  // 定期获取日志
  setInterval(() => {
    fetchLogs();
  }, props.refreshInterval);
});

// 监听 logs 的变化，将其保存到 localStorage
watch(logs, (newLogs) => {
  localStorage.setItem('logs', JSON.stringify(newLogs)); // 将最新日志保存到 localStorage
});
</script>

<template>
  <div class="log-container">
    <h1 class="title">终端日志</h1>
    <ul class="log-list">
      <li v-for="(log, index) in logs" :key="index" class="log-item">{{ log }}</li>
    </ul>
  </div>
</template>

<style scoped>
/* 深色背景的整体样式 */
.log-container {
  background-color: #333844;
  color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  font-family: 'Arial', sans-serif;
  max-width: 500px;
  max-height: 400px;
  margin: 20px auto;
}

/* 标题样式 */
.title {
  font-size: 24px;
  font-weight: bold;
  color: #C5C5C5;
  margin-bottom: 16px;
  text-align: center;
}

/* 日志列表样式 */
.log-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #444;
  border-radius: 10px;
  background-color: #1b1d22;
}

/* 每个日志条目样式 */
.log-item {
  padding: 8px 12px;
  border-radius: 4px;
  border-bottom: 1px solid #444;
  font-size: 14px;
  line-height: 1.5;
  color: #ddd;
}

.log-item:last-child {
  border-bottom: none;
}

/* 鼠标悬停日志条目效果 */
.log-item:hover {
  background-color: #2a2d35;
  color: #b4b4b4;
}

/* 日志列表的滚动条样式 */
.log-list::-webkit-scrollbar {
  width: 8px;
}

.log-list::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.log-list::-webkit-scrollbar-thumb:hover {
  background: #888;
}
</style>
