<template>
  <div class="vtk-viewer">
    <input type="file" accept=".vtp" @change="handleFileUpload" />
    <div ref="vtkContainer" class="viewer-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import '@kitware/vtk.js/Rendering/Profiles/Geometry'
import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader'
import vtkMapper from '@kitware/vtk.js/Rendering/Core/Mapper'
import vtkActor from '@kitware/vtk.js/Rendering/Core/Actor'
import vtkRenderWindow from '@kitware/vtk.js/Rendering/Core/RenderWindow'
import vtkRenderer from '@kitware/vtk.js/Rendering/Core/Renderer'
import vtkRenderWindowInteractor from '@kitware/vtk.js/Rendering/Core/RenderWindowInteractor'
import vtkOpenGLRenderWindow from '@kitware/vtk.js/Rendering/OpenGL/RenderWindow'
import vtkInteractorStyleTrackballCamera from '@kitware/vtk.js/Interaction/Style/InteractorStyleTrackballCamera'
import vtkPointPicker from '@kitware/vtk.js/Rendering/Core/PointPicker'

import vtkLight from '@kitware/vtk.js/Rendering/Core/Light'

const vtkContainer = ref(null)
let renderWindow
let renderer
let openGLRenderWindow
let renderWindowInteractor
let interactorStyle

// 初始化VTK渲染器
onMounted(() => {
  if (!vtkContainer.value) return

  // 创建渲染窗口和渲染器
  renderWindow = vtkRenderWindow.newInstance()
  renderer = vtkRenderer.newInstance()
  renderWindow.addRenderer(renderer)

  // 创建OpenGL渲染窗口
  openGLRenderWindow = vtkOpenGLRenderWindow.newInstance()
  renderWindow.addView(openGLRenderWindow)

  // 设置容器
  openGLRenderWindow.setContainer(vtkContainer.value)

  // 创建交互器
  renderWindowInteractor = vtkRenderWindowInteractor.newInstance()
  renderWindowInteractor.setView(openGLRenderWindow)
  renderWindowInteractor.setInteractorStyle(
    vtkInteractorStyleTrackballCamera.newInstance()
  )
  renderWindowInteractor.initialize()

  // 设置深色背景以提升对比度
  renderer.setBackground(0.1, 0.1, 0.15)  // 深蓝灰色背景
  renderer.setTwoSidedLighting(true)      // 启用双面光照

  // 设置容器大小
  const { width, height } = vtkContainer.value.getBoundingClientRect()
  openGLRenderWindow.setSize(width, height)

  // 确保交互器绑定到容器
  renderWindowInteractor.bindEvents(vtkContainer.value)

  // 绑定窗口大小改变事件
  window.addEventListener('resize', resizeRenderer)
})

// 清理资源
onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeRenderer)
  
  if (renderWindowInteractor) {
    renderWindowInteractor.delete()
  }
  if (openGLRenderWindow) {
    openGLRenderWindow.delete()
  }
  if (renderWindow) {
    renderWindow.delete()
  }
})

// 更新渲染器大小
const resizeRenderer = () => {
  if (!vtkContainer.value || !openGLRenderWindow) return
  const { width, height } = vtkContainer.value.getBoundingClientRect()
  openGLRenderWindow.setSize(width, height)
  renderWindow.render()
}

// 处理文件上传
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = async (e) => {
    try {
      // 创建VTP读取器
      const vtpReader = vtkXMLPolyDataReader.newInstance()
      
      // 解析VTP数据
      vtpReader.parseAsArrayBuffer(e.target.result)
      const polyData = vtpReader.getOutputData()

      // 创建映射器和演员
      const mapper = vtkMapper.newInstance()
      mapper.setInputData(polyData)
      
      const actor = vtkActor.newInstance()
      actor.setMapper(mapper)

      // 获取RGB颜色数组
      const rgbArray = polyData.getPointData().getArrayByName('RGB')
      if (rgbArray) {
        // 设置使用直接RGB颜色而不是标量映射
        mapper.setScalarVisibility(true)
        mapper.setColorModeToDirectScalars()
        
        // 确保颜色数组被设置为活动标量
        polyData.getPointData().setScalars(rgbArray)
      } else {
        console.warn('No RGB array found in the point data')
      }

      // 设置点的大小
      actor.getProperty().setPointSize(3)
      
      // 模仿 PyVista 的渲染效果
      const property = actor.getProperty()
      
      // 光照参数调整
      property.setAmbient(0.4)         // 较低的环境光，增加对比度
      property.setDiffuse(0.6)         // 增加漫反射，增强立体感
      property.setSpecular(0.15)       // 适度的镜面反射
      property.setSpecularPower(100)   // 较高的镜面反射功率，控制高光范围
      
      // 渲染质量设置
      property.setInterpolation(1)     // 使用 Phong 着色
      property.setEdgeVisibility(false)// PyVista 默认不显示边缘
      property.setPointSize(12)         // 适中的点大小
      
      // 设置光照计算方式
      renderer.setTwoSidedLighting(true)  // 启用双面光照
      renderer.setLightFollowCamera(true) // 光源跟随相机
      
      // 添加第二个光源以增强立体感
      const light2 = vtkLight.newInstance()
      light2.setPositional(true)
      light2.setLightType('SceneLight')
      light2.setIntensity(0.6)
      light2.setPosition(1, 2, 3)
      light2.setFocalPoint(0, 0, 0)
      light2.setColor(1, 1, 1)
      renderer.addLight(light2)
      
      // 清除现有的actors并添加新的actor
      renderer.removeAllViewProps()
      renderer.addActor(actor)
      
      // 重置相机并渲染
      renderer.resetCamera()
      renderWindow.render()
    } catch (error) {
      console.error('Error loading VTP file:', error)
    }
  }

  reader.readAsArrayBuffer(file)
}
</script>

<style scoped>
.vtk-viewer {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.viewer-container {
  flex: 1;
  min-height: 0;
  position: relative;
  background-color: white;
}

/* 确保输入框在顶部且不会被遮挡 */
input[type="file"] {
  margin: 10px;
  z-index: 1;
}
</style>