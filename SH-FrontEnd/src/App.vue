<template>
  <div class="body">
    <TopBar class="top-bar" />
    <div class="sider-bar">

      <router-link to="/set" class="nav-link" title="配置">
        <img src="@/assets/app/setting.svg" alt="配置" class="icon" />
      </router-link>

      <router-link to="/test" class="nav-link" title="详细">
        <img src="@/assets/app/terminal.svg" alt="模型" class="icon" style="margin-left: 10px;"/>
      </router-link>

    </div>
    <router-view></router-view>
  
    <!-- <div class="log-view"></div> -->
  </div>
</template>

<script setup>

</script>

<style lang="less" scoped>
.body {
  width: 100%;
  height: 100%;
  display: flex;
  background-color: #282C34;
}

.top-bar {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  height: 30px;
  background-color: #323844;
  position: fixed;
  z-index: 0; /* 设置高的 z-index 值，使其置顶 */
}
.sider-bar{
  margin-top:30px;
  display: flex;
  flex-direction: column;
}
.icon{

  margin: 5px;
  cursor: pointer;
  transition: background-color 0.3s, opacity 0.3s, color 0.3s, scale 0.3s;
  &:hover {
    color: #7860e3;
    scale: 1.1;
  }

}
</style>