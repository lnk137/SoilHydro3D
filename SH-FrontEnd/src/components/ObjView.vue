<!-- OBJViewer.vue -->
<script setup>
import { ref, shallowRef, onMounted, onBeforeUnmount } from 'vue'
import * as THREE from 'three'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

// DOM 引用
const containerRef = ref(null)
const fileInput = ref(null)

// Three.js 相关对象
const scene = shallowRef(null)
const camera = shallowRef(null)
const renderer = shallowRef(null)
const controls = shallowRef(null)
const currentModel = shallowRef(null)

// 加载状态
const isLoading = ref(false)
const loadingProgress = ref(0)

// 场景初始化
const initScene = () => {
  scene.value = new THREE.Scene()
  scene.value.background = new THREE.Color(0xf0f0f0)

  // 相机设置
  camera.value = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  )
  camera.value.position.z = 100

  // 渲染器设置
  renderer.value = new THREE.WebGLRenderer({ 
    antialias: true,
    logarithmicDepthBuffer: true // 添加对数深度缓冲
  })
  renderer.value.setSize(window.innerWidth, window.innerHeight)
  renderer.value.outputEncoding = THREE.sRGBEncoding
  renderer.value.setPixelRatio(window.devicePixelRatio)
  containerRef.value.appendChild(renderer.value.domElement)

  // 控制器设置
  controls.value = new OrbitControls(camera.value, renderer.value.domElement)
  controls.value.enableDamping = true
  controls.value.dampingFactor = 0.05
  controls.value.rotateSpeed = 0.5
  controls.value.enablePan = true
  controls.value.enableZoom = true

  // 光源设置
  const ambientLight = new THREE.AmbientLight(0x808080)
  scene.value.add(ambientLight)

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(1, 1, 1)
  scene.value.add(directionalLight)

  const backLight = new THREE.DirectionalLight(0xffffff, 0.3)
  backLight.position.set(-1, -1, -1)
  scene.value.add(backLight)

  animate()
}

// 动画循环
const animate = () => {
  if (!renderer.value || !scene.value || !camera.value) return
  
  requestAnimationFrame(animate)
  if (controls.value) controls.value.update()
  renderer.value.render(scene.value, camera.value)
}

// 窗口大小变化处理
const handleResize = () => {
  if (!camera.value || !renderer.value) return

  camera.value.aspect = window.innerWidth / window.innerHeight
  camera.value.updateProjectionMatrix()
  renderer.value.setSize(window.innerWidth, window.innerHeight)
}

// 加载模型和材质
const loadModelWithMaterials = async (objFile, mtlFile) => {
  try {
    isLoading.value = true
    loadingProgress.value = 0

    // 创建加载器
    const objLoader = new OBJLoader()
    const mtlLoader = new MTLLoader()

    // 如果有 MTL 文件，先加载材质
    if (mtlFile) {
      const mtlBlob = new Blob([await mtlFile.arrayBuffer()], { type: 'text/plain' })
      const mtlUrl = URL.createObjectURL(mtlBlob)
      
      try {
        const materials = await new Promise((resolve, reject) => {
          mtlLoader.load(mtlUrl, resolve, 
            // 进度回调
            (xhr) => {
              loadingProgress.value = (xhr.loaded / xhr.total) * 40
            }, 
            reject
          )
        })
        
        materials.preload()
        objLoader.setMaterials(materials)
      } finally {
        URL.revokeObjectURL(mtlUrl)
      }
    }

    // 加载 OBJ 文件
    const objBlob = new Blob([await objFile.arrayBuffer()], { type: 'text/plain' })
    const objUrl = URL.createObjectURL(objBlob)

    try {
      const object = await new Promise((resolve, reject) => {
        objLoader.load(objUrl, resolve, 
          // 进度回调
          (xhr) => {
            loadingProgress.value = 40 + (xhr.loaded / xhr.total) * 60
          }, 
          reject
        )
      })

      // 清理当前模型
      if (currentModel.value) {
        scene.value.remove(currentModel.value)
        currentModel.value.traverse((child) => {
          if (child.geometry) child.geometry.dispose()
          if (child.material) {
            if (Array.isArray(child.material)) {
              child.material.forEach(material => material.dispose())
            } else {
              child.material.dispose()
            }
          }
        })
      }

      // 自动调整模型位置和大小
      const box = new THREE.Box3().setFromObject(object)
      const size = box.getSize(new THREE.Vector3())
      const center = box.getCenter(new THREE.Vector3())

      object.position.sub(center) // 居中模型

      // 调整相机位置以适应模型大小
      const maxDim = Math.max(size.x, size.y, size.z)
      const fov = camera.value.fov * (Math.PI / 180)
      let cameraZ = Math.abs(maxDim / Math.tan(fov / 2))
      cameraZ *= 1.5 // 添加一些边距
      
      camera.value.position.z = cameraZ
      camera.value.near = cameraZ / 100
      camera.value.far = cameraZ * 100
      camera.value.updateProjectionMatrix()

      // 更新控制器
      controls.value.target.set(0, 0, 0)
      controls.value.update()

      currentModel.value = object
      scene.value.add(object)

    } finally {
      URL.revokeObjectURL(objUrl)
    }

  } catch (error) {
    console.error('加载模型出错:', error)
    throw error
  } finally {
    isLoading.value = false
    loadingProgress.value = 100
  }
}

// 处理文件上传
const handleFileUpload = async (event) => {
  const files = event.target.files
  if (!files.length || !scene.value) return

  const objFile = Array.from(files).find(file => file.name.toLowerCase().endsWith('.obj'))
  const mtlFile = Array.from(files).find(file => file.name.toLowerCase().endsWith('.mtl'))

  if (!objFile) {
    console.error('未找到 OBJ 文件')
    return
  }

  try {
    await loadModelWithMaterials(objFile, mtlFile)
  } catch (error) {
    console.error('处理文件时出错:', error)
  }
}

// 生命周期钩子
onMounted(() => {
  initScene()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  
  // 清理资源
  if (renderer.value) {
    renderer.value.dispose()
    renderer.value.forceContextLoss()
    renderer.value.domElement.remove()
  }
  
  if (currentModel.value) {
    currentModel.value.traverse((child) => {
      if (child.geometry) child.geometry.dispose()
      if (child.material) {
        if (Array.isArray(child.material)) {
          child.material.forEach(material => material.dispose())
        } else {
          child.material.dispose()
        }
      }
    })
  }
  
  if (controls.value) {
    controls.value.dispose()
  }

  // 清理 Three.js 缓存
  const textureCache = renderer.value?.info.memory.textures || 0
  const geometryCache = renderer.value?.info.memory.geometries || 0
  
  if (textureCache > 0 || geometryCache > 0) {
    console.warn(`清理残留缓存: ${textureCache} 纹理, ${geometryCache} 几何体`)
    THREE.Cache.clear()
  }
})
</script>

<template>
  <div class="obj-viewer">
    <div class="file-upload">
      <input
        ref="fileInput"
        type="file"
        accept=".obj,.mtl"
        multiple
        @change="handleFileUpload"
      />
      <div v-if="isLoading" class="loading-progress">
        加载进度: {{ loadingProgress.toFixed(1) }}%
      </div>
    </div>
    <div ref="containerRef" class="viewer-container"></div>
  </div>
</template>

<style scoped>
.obj-viewer {
  width: 100%;
  height: 100vh;
  position: relative;
}

.file-upload {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 100;
  background: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading-progress {
  margin-top: 8px;
  font-size: 14px;
  color: #666;
}

.viewer-container {
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, #e0e0e0, #f5f5f5);
}
</style>