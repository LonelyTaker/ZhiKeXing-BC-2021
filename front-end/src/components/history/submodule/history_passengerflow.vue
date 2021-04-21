<template>
  <div id="history_passenger_flow">
    <div id="title">
      <p>客流量数据</p>
      <!-- 选择日期 -->
      <div id="choose_time">
        <el-button type="button" @click="startdate_dialogVisible = true" style="box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.16);">选择起始时间</el-button>
        <el-dialog title="起始时间" :visible.sync="startdate_dialogVisible" :append-to-body="true">
          <el-calendar v-model="start_date"> </el-calendar>
        </el-dialog>
        <el-button type="button" @click="enddate_dialogVisible = true" style="box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.16);">选择结束时间</el-button>
        <el-dialog title="结束时间" :visible.sync="enddate_dialogVisible" :append-to-body="true">
          <el-calendar v-model="end_date"> </el-calendar>
        </el-dialog>
      </div>
      <el-cascader id="select" v-model="value" :options="options" :props="{ expandTrigger: 'hover' }" @change="StaChange" placeholder="请选择站点"> </el-cascader>
    </div>
    <!-- 文字信息 -->
    <div id="info">
      <div class="info_div">
        <div class="info_icon">
          <img src="@/assets/platform.png" />
        </div>
        <div class="info_p">
          <p>站点名称:</p>
          <p style="font-size: 27px;">{{ sta_name }}</p>
        </div>
      </div>
      <div class="info_div">
        <div class="info_icon">
          <img src="@/assets/section.png" />
        </div>
        <div class="info_p">
          <p>全部客流量:</p>
          <p style="font-size: 27px;">{{ all_passengerflow }}人</p>
        </div>
      </div>
      <div class="info_div">
        <div class="info_icon">
          <img src="@/assets/crowding.png" style="width: 40%;height: 60%;top: 20%;left: 30%;" />
        </div>
        <div class="info_p">
          <p>最大拥挤度:</p>
          <p style="font-size: 27px;">{{ max_crowding }}%</p>
        </div>
      </div>
      <div id="info_time">
        <p>起始时间：{{ start_date | timeFormat }}</p>
        <p>结束时间：{{ end_date | timeFormat }}</p>
      </div>
    </div>
    <!-- 图表区域 -->
    <div id="mycharts"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sta_name: 'Sta157', // 初始站点名称
      all_passengerflow: 0, // 全部客流量
      max_crowding: '40', // 最大拥挤度
      value: [0, 0], // 下拉菜单默认选择‘Sta157’站点
      options: [], // 车站列表
      startdate_dialogVisible: false,
      enddate_dialogVisible: false,
      start_date: '2020-05-01', // 开始时间
      end_date: '2020-06-30', // 结束时间
      timeList: [], // 时间列表
      flowInList: [], // 历史进站客流列表
      flowOutList: [] // 历史出站客流列表
    }
  },
  methods: {
    // 监听站点改变
    StaChange(value) {
      if (value.length > 0) {
        this.sta_name = this.options[value[0]].children[value[1]].label
        if (this.timeFormat(this.start_date) === this.timeFormat(this.end_date)) {
          this.getHistoryFlowHour()
        } else {
          this.getHistoryFlow()
        }
      }
    },
    // 绘图
    init_chart() {
      let myChart = this.$echarts.init(document.getElementById('mycharts'))
      let option = {
        title: {
          text: '客流量数据',
          subtext: '单位（人）',
          textStyle: {
            color: '#143689',
            fontSize: 23,
            fontWeight: 'bold'
          },
          subtextStyle: {
            color: '#143689',
            fontSize: 17,
            fontWeight: 'bold'
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['进站', '出站'],
          textStyle: {
            fontSize: 19,
            fontWeight: 'bold',
            color: '#143689'
          }
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: this.timeList,
          axisLabel: {
            fontSize: 19,
            align: 'left',
            lineHeight: 56,
            color: '#143689'
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value}',
            fontSize: 19,
            color: '#143689'
          }
        },
        series: [
          {
            name: '进站',
            type: 'line',
            data: this.flowInList,
            lineStyle: {
              width: 3
            },
            symbol: 'none'
          },
          {
            name: '出站',
            type: 'line',
            data: this.flowOutList,
            lineStyle: {
              width: 3
            },
            symbol: 'none'
          }
        ],
        color: ['#505ED0', '#FF6060']
      }
      myChart.setOption(option)
    },
    // 获取历史客流数据
    getHistoryFlow() {
      this.$axios
        .get('http://localhost:54418//api/historyflow', { params: { startDate: this.start_date, endDate: this.end_date, staName: this.sta_name } })
        .then(res => {
          res = res.data
          this.all_passengerflow = 0
          this.timeList.length = 0
          this.flowInList.length = 0
          this.flowOutList.length = 0
          res.forEach(item => {
            this.timeList.push(this.timeFormat(item.date))
            this.flowInList.push(item.flow_in)
            this.flowOutList.push(item.flow_out)
            this.all_passengerflow += item.flow_in + item.flow_out
          })
          this.init_chart()
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 获取历史客流数据（某一天）
    getHistoryFlowHour() {
      this.$axios
        .get('http://localhost:54418//api/historyflowhour', { params: { date: this.start_date, staName: this.sta_name } })
        .then(res => {
          res = res.data
          this.all_passengerflow = 0
          this.timeList.length = 0
          this.flowInList.length = 0
          this.flowOutList.length = 0
          res.forEach(item => {
            this.timeList.push(this.timeFormat(item.date) + ' ' + item.hour + '时')
            this.flowInList.push(item.flow_in)
            this.flowOutList.push(item.flow_out)
            this.all_passengerflow += item.flow_in + item.flow_out
          })
          this.init_chart()
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 时间格式化
    timeFormat(time) {
      var dt = new Date(time)
      var y = dt.getFullYear()
      var m = (dt.getMonth() + 1).toString().padStart(2, '0')
      var d = dt
        .getDate()
        .toString()
        .padStart(2, '0')
      return `${y}-${m}-${d}`
    }
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
  },
  mounted() {
    this.$nextTick(() => {
      this.getHistoryFlow()
    })
  },
  filters: {
    timeFormat: function(time) {
      var dt = new Date(time)
      var y = dt.getFullYear()
      var m = (dt.getMonth() + 1).toString().padStart(2, '0')
      var d = dt
        .getDate()
        .toString()
        .padStart(2, '0')
      return `${y}-${m}-${d}`
    }
  },
  watch: {
    start_date(newVal) {
      if (this.timeFormat(newVal) === this.timeFormat(this.end_date)) {
        this.getHistoryFlowHour()
      } else {
        this.getHistoryFlow()
      }
      this.startdate_dialogVisible = false
    },
    end_date(newVal) {
      if (this.timeFormat(newVal) === this.timeFormat(this.start_date)) {
        this.getHistoryFlowHour()
      } else {
        this.getHistoryFlow()
      }
      this.enddate_dialogVisible = false
    }
  }
}
</script>

<style scoped>
/* 客流数据标签页 */
#history_passenger_flow {
  width: 100%;
  height: 100%;
  padding: 20px 40px 40px 40px;
}
#title {
  width: 100%;
  height: 60px;
}
#title > p {
  float: left;
  width: 160px;
  font-size: 32px;
  font-weight: bold;
  color: #143689;
  margin: 0px;
  transform: translateY(18%);
}
#select {
  float: right;
  transform: translateY(25%);
  box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.16);
}
#choose_time {
  height: 100%;
  float: right;
  width: 280px;
  padding: 10px;
}
/* 文字信息 */
#info {
  width: 100%;
  height: 13%;
}
.info_div {
  float: left;
  height: 100%;
  width: 18%;
  padding: 10px;
  position: relative;
}
.info_icon {
  width: 60px;
  height: 60px;
  position: absolute;
  top: 10%;
  background-color: #505ed0;
  border-radius: 30px;
}
.info_icon > img {
  position: absolute;
  top: 25%;
  left: 25%;
  height: 50%;
  width: 50%;
}
.info_p {
  position: absolute;
  top: 14%;
  width: 100%;
  padding-left: 70px;
}
.info_p > p {
  font-size: 13px;
  font-weight: bold;
  color: #143689;
  margin: 0px;
}
#info_time {
  height: 100%;
  width: 280px;
  padding-left: 35px;
  padding-top: 8px;
  float: right;
  font-size: 21px;
  font-weight: bold;
  line-height: 27px;
  color: #143689;
}
/* 图表区域 */
#mycharts {
  width: 100%;
  height: 80%;
  padding: 20px;
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.16);
}
</style>
<style>
.el-button + .el-button {
  margin: 0px;
}
</style>
