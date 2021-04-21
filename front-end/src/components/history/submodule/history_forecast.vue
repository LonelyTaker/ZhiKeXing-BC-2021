<template>
  <div id="history_forecast">
    <div id="title">
      <p>历史预测记录</p>
      <el-cascader id="select" v-model="value" :options="options" :props="{ expandTrigger: 'hover' }" @change="StaChange" placeholder="请选择站点"> </el-cascader>
    </div>
    <div id="table">
      <el-table id="forecast_table" :data="tableData" stripe>
        <el-table-column prop="date" label="预测日期"> </el-table-column>
        <el-table-column prop="staName" label="站点"> </el-table-column>
        <el-table-column prop="forecastIn" label="预测进站人数"> </el-table-column>
        <el-table-column prop="forecastOut" label="预测出站人数"> </el-table-column>
        <el-table-column prop="forecastError" label="精确度"> </el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      staName: 'Sta157',
      value: [],
      options: [],
      tableData: []
    }
  },
  methods: {
    StaChange(value) {
      this.staName = this.options[value[0]].children[value[1]].label
      this.tableData.length = 0
      this.$axios
        .get('https://localhost:44308/api/historyforecast', { params: { staName: this.staName } })
        .then(res => {
          res = res.data
          res.forEach(item => {
            let el = {
              date: this.timeFormat(item.date),
              staName: item.staName,
              forecastIn: item.forecastIn + '人',
              forecastOut: item.forecastOut + '人',
              forecastError: item.forecastError * 100 + '%'
            }
            this.tableData.push(el)
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    timeFormat(time) {
      var dt = new Date(time)
      var y = dt.getFullYear()
      var m = (dt.getMonth() + 1).toString().padStart(2, '0')
      var d = dt
        .getDate()
        .toString()
        .padStart(2, '0')
      return `${y}-${m}-${d}`
    },
    init() {
      this.$axios
        .get('https://localhost:44308/api/historyforecast')
        .then(res => {
          res = res.data
          res.forEach(item => {
            let el = {
              date: this.timeFormat(item.date),
              staName: item.staName,
              forecastIn: item.forecastIn + '人',
              forecastOut: item.forecastOut + '人',
              forecastError: item.forecastError * 100 + '%'
            }
            this.tableData.push(el)
          })
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  mounted() {
    this.init()
  },
  async created() {
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
}
</script>
<style scoped>
#history_forecast {
  height: 100%;
  width: 100%;
  padding: 30px;
  padding-top: 10px;
}
/* title部分 */
#title {
  width: 100%;
  height: 75px;
}
#title > p {
  float: left;
  width: 192px;
  height: 100%;
  font-size: 32px;
  line-height: 100%;
  font-weight: bold;
  color: #143689;
  margin: 0px;
  transform: translateY(21.5px);
}
#select {
  height: 100%;
  float: right;
  transform: translateY(17.5px);
}
/* 图表部分 */
#table {
  width: 100%;
  height: 90%;
  padding: 10px;
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.16);
}
#forecast_table {
  width: 100%;
  height: 100%;
  overflow: scroll;
  overflow-x: hidden;
}
</style>
