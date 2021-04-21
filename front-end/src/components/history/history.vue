<template>
  <div id="history">
    <el-tabs type="card">
      <el-tab-pane label="地铁客流数据" style="background-color:white;"><my-passengerflow></my-passengerflow></el-tab-pane>
      <el-tab-pane label="乘客信息查询" style="background-color:white;"><my-passengerinfo></my-passengerinfo></el-tab-pane>
      <el-tab-pane label="用户出行图" style="background-color:white;"><my-OD></my-OD></el-tab-pane>
      <el-tab-pane label="历史预测记录" style="background-color:white;"><my-forecast></my-forecast></el-tab-pane>
    </el-tabs>
  </div>
</template>
<script>
import HistoryPF from './submodule/history_passengerflow.vue'
import HistoryPI from './submodule/history_passengerinfo.vue'
import HistoryF from './submodule/history_forecast.vue'
import OD from './submodule/OD.vue'
export default {
  data() {
    return {}
  },
  methods: {},
  components: {
    'my-passengerflow': HistoryPF,
    'my-passengerinfo': HistoryPI,
    'my-forecast': HistoryF,
    'my-OD': OD
  }
}
</script>
<style scoped>
#history {
  width: 100%;
  height: 100%;
}
</style>
<style>
/* 修改标签页默认样式 */
.el-tabs__item {
  color: #143689;
  background-color: #ffffff;
  border-radius: 10px 10px 0 0;
  font-weight: bold;
  font-size: 19px;
}
.el-tabs__item.is-active {
  background-color: #143689;
  color: #ffffff;
  font-weight: bold;
}
.el-tabs--card > .el-tabs__header .el-tabs__item {
  border: none;
  margin: 0 10px 0 0;
}
.el-tabs--card > .el-tabs__header .el-tabs__nav {
  border: none;
}
.el-tabs--card > .el-tabs__header {
  border: none;
}
.el-tabs__header {
  margin: 0px;
}
.el-tabs.el-tabs--card.el-tabs--top {
  height: 100%;
}
.el-tabs__content {
  height: 93%;
}
.el-tab-pane {
  height: 100%;
}
</style>
