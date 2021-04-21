<template>
  <div id="forecast_sta">
    <div id="title">
      <p>客流量预测</p>
    </div>
    <div id="info">
      <div>
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
            <p>预测进站客流量:</p>
            <p style="font-size: 27px;">{{ sta_section_in }}人</p>
          </div>
        </div>
        <div class="info_div">
          <div class="info_icon">
            <img src="@/assets/gate.png" />
          </div>
          <div class="info_p">
            <p>预测出站客流量:</p>
            <p style="font-size: 27px;">{{ sta_section_out }}人</p>
          </div>
        </div>
        <div class="info_div">
          <div class="info_icon">
            <img src="@/assets/crowding.png" style="width:40%" />
          </div>
          <div class="info_p">
            <p>预测最大拥挤度:</p>
            <p style="font-size: 27px;">40%</p>
          </div>
        </div>
      </div>
      <div id="switchArea">
        <el-switch v-model="way" active-text="日客流预测" inactive-text="小时客流预测" active-color="#505ed0" inactive-color="#505ed0" @change="switchChange"> </el-switch>
      </div>
    </div>
    <div id="chart"></div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      way: false,
      sta_name: '',
      sta_section_in: 0, // 进站人数
      sta_section_out: 0, // 出站站人数
      xlist: [], // 横坐标
      sta_in: [], // 进站列表
      sta_out: [], // 出站列表
      reality_in: [], // 当日出站数据(小时)
      reality_out: [] // 当日进站数据(小时)
    }
  },
  methods: {
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
    },
    // 绘制图表
    init_chart() {
      this.myChart = this.$echarts.init(document.getElementById('chart'))
      this.option = {
        title: {
          text: '客流量预计',
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
          data: ['预测进站', '预测出站', '进站', '出站'],
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
          data: this.xlist,
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
            name: '预测进站',
            type: 'line',
            data: this.sta_in,
            lineStyle: {
              width: 3,
              type: 'dashed'
            },
            symbol: 'none'
          },
          {
            name: '预测出站',
            type: 'line',
            data: this.sta_out,
            lineStyle: {
              width: 3,
              type: 'dashed'
            },
            symbol: 'none'
          },
          {
            name: '进站',
            type: 'line',
            data: this.reality_in,
            lineStyle: {
              width: 3
            },
            symbol: 'none'
          },
          {
            name: '出站',
            type: 'line',
            data: this.reality_out,
            lineStyle: {
              width: 3
            },
            symbol: 'none'
          }
        ],
        color: ['rgba(80,94,208,0.5)', 'rgba(255,96,96,0.5)', '#505ED0', '#FF6060']
      }
      this.myChart.setOption(this.option)
    },

    // 获取下周预测数据
    getDaily() {
      this.$axios
        .get('http://localhost:54418//api/forecastdaily', { params: { staName: this.sta_name } })
        .then(res => {
          this.sta_in.length = 0
          this.sta_out.length = 0
          this.sta_section_in = 0
          this.sta_section_out = 0
          this.xlist.length = 0

          res.data.forEach(item => {
            this.xlist.push(this.timeFormat(item.date))
            this.sta_in.push(item.forecastIn)
            this.sta_section_in += item.forecastIn
            this.sta_out.push(item.forecastOut)
            this.sta_section_out += item.forecastOut
          })

          this.$axios
            .get('http://localhost:54418//api/historyflow', { params: { startDate: '2020-06-24', endDate: '2020-06-30', staName: this.sta_name } })
            .then(res => {
              res = res.data

              this.reality_in.length = 0
              this.reality_out.length = 0
              res.forEach(item => {
                this.reality_in.push(item.flow_in)
                this.reality_out.push(item.flow_out)
              })
              this.init_chart()
            })
            .catch(err => {
              console.log(err)
            })
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 获取明日预测数据
    getHour() {
      this.$axios
        .get('http://localhost:54418//api/forecasthour', { params: { staName: this.sta_name } })
        .then(res => {
          this.sta_in.length = 0
          this.sta_out.length = 0
          this.sta_section_in = 0
          this.sta_section_out = 0
          this.xlist.length = 0
          res.data.forEach(item => {
            this.xlist.push(this.timeFormat(item.date) + ' ' + item.hour + '时')
            this.sta_in.push(item.forecastIn)
            this.sta_section_in += item.forecastIn
            this.sta_out.push(item.forecastOut)
            this.sta_section_out += item.forecastOut
          })

          this.$axios
            .get('http://localhost:54418//api/historyflowhour', { params: { date: '2020-07-01', staName: this.sta_name } })
            .then(res => {
              res = res.data

              this.reality_in.length = 0
              this.reality_out.length = 0
              for (let i = 0; i < 18; ++i) {
                this.reality_in.push(res[i].flow_in)
                this.reality_out.push(res[i].flow_out)
              }

              this.init_chart()
            })
            .catch(err => {
              console.log(err)
            })
        })
        .catch(err => {
          console.log(err)
        })
    },

    // 初始化
    init(staName) {
      this.sta_name = staName
      if (this.way) {
        this.getDaily()
      } else {
        this.getHour()
      }
    },
    // 监听开关改变
    switchChange() {
      if (this.way) {
        this.getDaily()
      } else {
        this.getHour()
      }
    }
  }
}
</script>
<style scoped>
#forecast_sta {
  width: 100%;
  height: 100%;
  padding: 30px 40px 20px 40px;
}
#title {
  width: 100%;
  height: 7%;
  display: flex;
  align-items: center;
}
#title > p {
  font-size: 32px;
  font-weight: bold;
  color: #143689;
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
  display: flex;
  justify-content: center;
  align-items: center;
}
.info_icon > img {
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
#switchArea {
  height: 80%;
  display: flex;
  align-items: center;
  justify-content: center;
}
/* 图表区域 */
#chart {
  width: 100%;
  height: 80%;
  padding: 20px;
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.16);
}
</style>
