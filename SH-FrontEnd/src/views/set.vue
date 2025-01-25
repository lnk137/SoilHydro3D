<template>
    <div class="body">
        <div class="container">
            <!-- 第一部分：路径选择 -->
            <div class="section">
                <div class="title">路径选择</div>
                <div class="row">
                    <div class="button" @click="select_file_path">选择图片文件夹</div>
                    <div class="button" @click="select_output_path">选择模型保存文件夹</div>
                </div>
            </div>

            <!-- 第二部分：模式选择 -->
            <div class="section">
                <div class="title">模式选择</div>
                <div class="row">
                    <el-select v-model="modelStore.target" placeholder="保留模式" size="large" style="width: 140px">
                        <el-option v-for="item in options_retentate" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                    <el-select v-model="modelStore.model_type" placeholder="生成模式" size="large" style="width: 140px">
                        <el-option v-for="item in options_type" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                </div>
            </div>

            <!-- 第三部分：滑块和文件名输入 -->
            <div class="section">
                <div class="title">配置参数</div>
                <div class="row">
                    <Slider />
                    <input v-model="pathStore.file_name" type="text" id="input" placeholder="输入保存文件名" title="保存文件名" />
                </div>
            </div>

            <!-- 第四部分：生成按钮 -->
            <div class="section">
                <div class="button generate" @click="creat_model">
                    <img src="@/assets/set/create.svg" alt="模型" class="icon" />
                    <span>生成模型</span>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref } from "vue";
import 'vue-multiselect/dist/vue-multiselect.css';

import { useUrlStore } from '@/stores/UrlStore';
import { usePathStore } from '@/stores/PathStore';
import { useModelStore } from '@/stores/ModelStore';

const urlStore = useUrlStore();
const pathStore = usePathStore();
const modelStore = useModelStore();



const options_retentate = [
    {
        value: '1',
        label: '无区分',
    },
    {
        value: 'preferential_flow',
        label: '优先流',
    },
    {
        value: 'matrix_flow',
        label: '基质流',
    },
]



const options_type = [
    {
        value: 'point_cloud',
        label: '点云',
    },
    {
        value: 'cube',
        label: '立方体',
    },
]

const select_file_path = async () => {
    const file_path = await select_get_folder_path();
    pathStore.file_path = file_path;
    console.log('imgpath',pathStore.file_path)
}
const select_output_path = async () => {
    const output_path = await select_get_folder_path();
    pathStore.output_path = output_path;
}

// 选择路径
const select_get_folder_path = async () => {
    try {
        const response = await fetch(`${urlStore.server_url}/file/get_folder_path`, {
            method: 'GET'
        });
        const data = await response.json();
        console.log('选择路径成功', data.folder_path);

        return data.folder_path;

    } catch (error) {
        console.error('选择路径失败', error);
    }
}
const checkField = (value, message) => {
    if (!value) {
        alert(message);
        return false;
    }
    return true;
};


const creat_model = async () => {
    try {
        if (
            !checkField(pathStore.file_path, '请选择图片文件夹！') ||
            !checkField(pathStore.output_path, '请选择模型保存文件夹！') ||
            !checkField(pathStore.file_name, '请输入保存文件名！') ||
            !checkField(modelStore.model_type, '请选择生成模式！') ||
            !checkField(modelStore.target, '请输入目标值！') ||
            !checkField(modelStore.layer_thickness, '请输入层厚度！')
        ) {
            return;
        }
        pathStore.full_path=pathStore.output_path+"/"+pathStore.file_name
        console.log(pathStore.full_path)
        alert('开始生成模型');
        const response = await fetch(`${urlStore.server_url}/creat/${modelStore.model_type}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                folder_path: pathStore.file_path,
                output_path: pathStore.full_path,
                target: modelStore.target,
                model_type: modelStore.model_type,
                layer_thickness: modelStore.layer_thickness,
            }),
        });

        const data = await response.json();
        console.log('生成模型结果', data);

    } catch (error) {
        console.error('生成模型失败', error);
    }
}
</script>

<style lang="less" scoped>
/* 主容器 */
.container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 400px;
    margin: auto;
}

/* 分区 */
.section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 15px;
    border: 1px solid #4b5264;
    border-radius: 10px;
    background-color: #2a2f38;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
}

/* 标题 */
.title {
    font-size: 16px;
    font-weight: bold;
    color: #c5c5c5;
    text-align: center;
    margin-bottom: 10px;
}

/* 行布局 */
.row {
    display: flex;
    gap: 15px;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
}

/* 按钮 */
.button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 160px;
    height: 40px;
    margin: 0;
    padding: 0;
    border-radius: 8px;
    background-color: #333844;
    color: #c5c5c5;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
    transition: all 0.3s;
}

.button:hover {
    background-color: #4b5264;
    scale: 1.05;
}

/* 输入框 */
input {
    all: unset;
    /* 移除所有默认样式 */
    width: 160px;
    height: 35px;
    color: #c5c5c5;
    background-color: #333844;
    border: 1px solid #4b5264;
    border-radius: 4px;
    text-align: center;
    transition: all 0.3s;
}

input:focus {
    border-color: #357d6e;
}

/* 滑块 */
.slider-demo-block {
    width: 100%;
}

.slider-demo-block .el-slider {
    margin-top: 0;
    margin-left: 12px;
}

/* 生成按钮样式 */
.generate {
    background-color: #2c685c;
    color: #fff;
}

.generate:hover {
    background-color: #318570;
    scale: 1.1;
}

.icon {
    width: 30px;
    height: 30px;
    margin-right: 8px;
}
</style>