<template>
  <div class="page">
    <div class="content">
      <LogViewer class="log-viewer" />
      <div class="button generate" @click="show_model">
        <img src="@/assets/terminal/show.svg" alt="模型" class="icon" />
        <span>显示模型</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useModelStore } from '@/stores/ModelStore';
import { useUrlStore } from '@/stores/UrlStore';

const modelStore = useModelStore();
const urlStore = useUrlStore();

const show_model = async () => {
    try {
        const response = await fetch(`${urlStore.server_url}/show/all`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              model_type: modelStore.model_type,
            }),
        });
        const data = await response.json();
        console.log('查看模型', data);

    } catch (error) {
        console.error('查看模型失败', error);
    }
}
</script>

<style lang="less" scoped>
.page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;

  gap: 20px;
}

.log-viewer {
  width: 600px;
  height: 400px;
  background-color: #2e3543;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
  padding: 16px;
  overflow-y: auto;
  color: #c5c5c5;
}

.button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 160px;
  height: 40px;
  border-radius: 8px;
  background-color: #3b3e4f;
  color: #ffffff;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s;
}

.button:hover {
  background-color: #43475b;
  transform: scale(1.05);
}

.icon {
  width: 30px;
  height: 30px;
  margin-right: 8px;
}
</style>
