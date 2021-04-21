<template>
  <div id="forecast">
    <div id="header">
      <div id="select">
        <!-- 站点选择 -->
        <el-cascader v-model="value" :options="options" :props="{ expandTrigger: 'hover' }" @change="StaChange" placeholder="请选择站点" clearable> </el-cascader>
      </div>
    </div>

    <div id="main">
      <forecast-map v-show="isMap"></forecast-map>
      <forecast-sta v-show="!isMap" ref="staInfo"></forecast-sta>
    </div>
  </div>
</template>

<script>
import ForecastMap from './submodule/forecast_map'
import ForecastSta from './submodule/forecast_sta'
export default {
  data() {
    return {
      isMap: true,
      value: [], // 当前下拉框选择的值
      options: [], // 车站列表
      sta_name: ''
    }
  },
  methods: {
    // 监听站点改变
    StaChange(value) {
      if (value.length > 0) {
        this.sta_name = this.options[value[0]].children[value[1]].label
        this.isMap = false
        this.$refs.staInfo.init(this.sta_name)
      } else {
        this.isMap = true
      }
    },
    // 获取车站列表
    async getStation() {
      const { data: res } = await this.$axios.get('http://localhost:54418/api/station')
      if (res.status === 1) {
        for (let i = 0; i < res.item.length; ++i) {
          let e1 = { value: i, label: res.item[i].line_name, children: [] }
          for (let j = 0; j < res.item[i].sta.length; ++j) {
            const e2 = { value: j, label: res.item[i].sta[j].sta_name }
            e1.children.push(e2)
          }
          this.options.push(e1)
        }
      }
    }
  },
  created() {
    this.getStation()
  },
  components: {
    'forecast-map': ForecastMap,
    'forecast-sta': ForecastSta
  }
}
</script>
<style scoped>
#forecast {
  width: 100%;
  height: 100%;
}
#header {
  width: 100%;
  height: 80px;
}
#select {
  float: left;
  transform: translateY(20px);
}
#main {
  width: 100%;
  height: 90%;
  background-color: white;
}
</style>
