<template>
    <div class="slider-group">
        <label for="slider">层厚度:{{ modelStore.layer_thickness }}</label>
        <input id="slider" type="range" v-model="modelStore.layer_thickness" :min="1" :max="10" :step="1" class="slider" />
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useModelStore } from '@/stores/ModelStore';

const modelStore = useModelStore();

// 绑定的值，初始为 1
const value = ref(1);
</script>

<style scoped>
.slider-group {
    display: flex;
    flex-direction: column;
    color: #C5C5C5;
    font-weight: bold;
    gap: 10px;
}

.slider {
    width: 100%;
    appearance: none;
    /* 移除默认样式 */
    height: 5px;
    background: #313641;
    border-radius: 5px;
    outline: none;
    transition: background 0.3s;
}

.slider::-webkit-slider-thumb {
    appearance: none;
    /* 移除默认样式 */
    width: 15px;
    height: 15px;
    background: #357D6E;
    /* 滑块颜色 */
    border-radius: 50%;
    cursor: pointer;
    transition: background 0.3s;
}

.slider::-webkit-slider-thumb:hover {
    background: #513a92;
    /* 鼠标悬停时的颜色 */
}

.slider:hover {
    background: #4d5567;
    /* 聚焦时的背景 */
}
</style>