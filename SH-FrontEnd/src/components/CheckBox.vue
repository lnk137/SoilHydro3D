<template>
    <div class="checkbox-group">
      <label class="container" v-for="option in options" :key="option.value">
        <input
          type="checkbox"
          :checked="selected === option.value"
          @change="handleChange(option.value)"
        />
        <div class="checkmark"></div>
        <span>{{ option.label }}</span>
      </label>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from "vue";
  
  // 接收父组件传递的选项和当前选中值
  defineProps({
    modelValue: {
      type: [String, null],
      default: null,
    },
    options: {
      type: Array,
      required: true,
      default: () => [],
    },
  });
  
  // 定义向父组件发送事件
  defineEmits(["update:modelValue", "change"]);
  
  // 初始化 selected 值
  const selected = ref(modelValue);
  
  // 监听父组件传递的 modelValue 的变化
  watch(() => modelValue, (newValue) => {
    selected.value = newValue;
  });
  
  // 处理选中逻辑
  const handleChange = (value) => {
    const newValue = selected.value === value ? null : value;
    selected.value = newValue;
  
    // 触发双向绑定和自定义事件
    emit("update:modelValue", newValue);
    emit("change", newValue);
  };
  </script>
  
  <style scoped>
  .checkbox-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .container {
    position: relative;
    cursor: pointer;
    display: flex;
    align-items: center;
  }
  
  .container input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
  }
  
  .checkmark {
    position: relative;
    width: 20px;
    height: 20px;
    border: 2px solid black;
    margin-right: 10px;
  }
  
  .checkmark:after {
    content: '';
    position: absolute;
    width: 10px;
    height: 10px;
    background-color: black;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    transition: transform 0.2s ease;
  }
  
  .container input:checked ~ .checkmark:after {
    transform: translate(-50%, -50%) scale(1);
  }
  </style>
  