<!-- VtkViewer.vue -->
<template>
    <div class="flex flex-col gap-4">
      <!-- 文件上传区域 -->
      <div class="border-2 border-dashed border-gray-300 p-4 rounded">
        <input
          type="file"
          accept=".vtk"
          @change="handleFileUpload"
          class="hidden"
          ref="fileInput"
        />
        <button 
          @click="triggerFileInput"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          选择 VTK 文件
        </button>
        <p v-if="fileName" class="mt-2">
          当前文件: {{ fileName }}
        </p>
      </div>
  
      <!-- 点云显示区域 -->
      <div 
        ref="vtkContainer" 
        class="w-full h-96 bg-gray-100 rounded"
      >
        <!-- VTK.js 渲染容器 -->
      </div>
  
      <!-- 控制面板 -->
      <div class="flex gap-4 items-center">
        <div class="flex items-center gap-2">
          <label>点大小:</label>
          <input
            type="range"
            v-model="pointSize"
            min="1"
            max="20"
            class="w-32"
          />
          <span>{{ pointSize }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  import '@kitware/vtk.js/Rendering/Profiles/Geometry'
  import vtkFullScreenRenderWindow from '@kitware/vtk.js/Rendering/Misc/FullScreenRenderWindow'
  import vtkActor from '@kitware/vtk.js/Rendering/Core/Actor'
  import vtkMapper from '@kitware/vtk.js/Rendering/Core/Mapper'
  import vtkPolyData from '@kitware/vtk.js/Common/DataModel/PolyData'
  import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader'
  
  // 响应式状态
  const fileName = ref('')
  const pointSize = ref(5)
  const fileInput = ref(null)
  const vtkContainer = ref(null)
  
  // VTK.js 相关变量
  let renderWindow = null
  let renderer = null
  let actor = null
  let mapper = null
  
  // 初始化 VTK.js 渲染器
  onMounted(() => {
    renderWindow = vtkFullScreenRenderWindow.newInstance({
      container: vtkContainer.value,
      background: [0.1, 0.1, 0.1],
    })
    
    renderer = renderWindow.getRenderer()
    renderWindow.getInteractor().setInteractorStyle('TrackballCamera')
    
    // 创建 actor 和 mapper
    actor = vtkActor.newInstance()
    mapper = vtkMapper.newInstance()
    actor.setMapper(mapper)
    renderer.addActor(actor)
  })
  
  // 清理资源
  onUnmounted(() => {
    if (renderWindow) {
      renderWindow.delete()
    }
  })
  
  // 触发文件选择
  const triggerFileInput = () => {
    fileInput.value.click()
  }
  
  // 处理文件上传
  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return
    
    fileName.value = file.name
    
    try {
      const arrayBuffer = await file.arrayBuffer()
      const reader = vtkXMLPolyDataReader.newInstance()
      reader.parseAsArrayBuffer(arrayBuffer)
      
      const polyData = reader.getOutputData()
      
      // 更新渲染
      mapper.setInputData(polyData)
      actor.getProperty().setPointSize(pointSize.value)
      
      // 重置相机位置
      renderer.resetCamera()
      renderWindow.render()
      
    } catch (error) {
      console.error('读取 VTK 文件时出错:', error)
    }
  }
  
  // 监听点大小变化
  watch(pointSize, (newSize) => {
    if (actor) {
      actor.getProperty().setPointSize(newSize)
      renderWindow?.render()
    }
  })
  </script>
  
  <style scoped>
  .vtk-container {
    position: relative;
    width: 100%;
    height: 100%;
  }
  </style>