<template>
  <div id="passengerinfo" ref="passengerinfo">
    <div id="header">
      <div id="title">
        <img src="@/assets/user_icon.png" />
        <p>用户信息查询</p>
      </div>
      <div id="select">
        <el-select v-model="line_value" placeholder="请选择站线" clearable @clear="reselect">
          <el-option v-for="line_item in line_options" :key="line_item.value" :label="line_item.label" :value="line_item.value"> </el-option>
        </el-select>
        <el-select v-model="station_value" placeholder="请选择站点" :disabled="is_disabled" @change="getStaData">
          <el-option v-for="station_item in station_options" :key="station_item.value" :label="station_item.label" :value="station_item.value"> </el-option>
        </el-select>
      </div>
    </div>
    <div id="table">
      <el-table :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" style="width: 100%;" height="500">
        <el-table-column prop="user_id" label="用户ID" width="300"> </el-table-column>
        <el-table-column prop="birthyear" label="年龄" width="130"> </el-table-column>
        <el-table-column prop="sex" label="性别"> </el-table-column>
      </el-table>
      <el-pagination background layout="prev, pager, next" :total="tableData.length" :page-size="pageSize" style="padding-top:10px" @current-change="handleCurrentChange"> </el-pagination>
    </div>
    <div id="chart" ref="chart"></div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      options: [],
      line_options: [],
      line_value: '',
      station_options: [],
      station_value: '',
      is_disabled: true,

      currentPage: 1, // 当前页
      pageSize: 100, // 每页条数
      tableData: [], // 表格数据
      myChart: null,
      roseData: [
        { value: 0, name: '2000-2009' },
        { value: 0, name: '1990-1999' },
        { value: 0, name: '1980-1989' },
        { value: 0, name: '1970-1979' },
        { value: 0, name: '1960-1969' },
        { value: 0, name: '1950-1959' },
        { value: 0, name: '1940-1949' },
        { value: 0, name: '1930-1939' }
      ] // 玫瑰图数据
    }
  },
  methods: {
    // 清空选择
    reselect() {
      this.is_disabled = true
      this.station_value = ''
      this.line_value = ''
      // 调用接口
    },
    // 选择站点
    getStaData() {
      // 调用接口
    },

    // 初始化图表
    init_chart() {
      this.myChart = this.$echarts.init(document.getElementById('chart'))
      let option = {
        title: {
          text: '用户年龄结构图'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b} : {c} ({d}%)'
        },
        legend: {
          left: 'center',
          top: 'bottom',
          data: ['2000-2009', '1990-1999', '1980-1989', '1970-1979', '1960-1969', '1950-1959', '1940-1949', '1930-1939']
        },
        series: [
          {
            name: '用户年龄结构',
            type: 'pie',
            radius: [20, 140],
            center: ['50%', '50%'],
            itemStyle: {
              borderRadius: 5
            },
            label: {
              show: true
            },
            emphasis: {
              label: {
                show: true
              }
            },
            data: this.roseData
          }
        ]
      }
      this.myChart.setOption(option)
    },
    // 获取用户信息
    getUserInfo() {
      this.$axios
        .get('https://localhost:44308/api/userinfo')
        .then(res => {
          res = res.data
          this.tableData = res
          this.tableData.forEach(item => {
            if (this.computeAge(String(item.birthyear)) < 20) {
              this.roseData[0].value++
            } else if (this.computeAge(String(item.birthyear)) < 30) {
              this.roseData[1].value++
            } else if (this.computeAge(String(item.birthyear)) < 40) {
              this.roseData[2].value++
            } else if (this.computeAge(String(item.birthyear)) < 50) {
              this.roseData[3].value++
            } else if (this.computeAge(String(item.birthyear)) < 60) {
              this.roseData[4].value++
            } else if (this.computeAge(String(item.birthyear)) < 70) {
              this.roseData[5].value++
            } else if (this.computeAge(String(item.birthyear)) < 80) {
              this.roseData[6].value++
            } else if (this.computeAge(String(item.birthyear)) < 90) {
              this.roseData[7].value++
            }
          })
          this.init_chart()
        })
        .catch(err => {
          console.log(err)
        })
    },

    // 计算年龄
    computeAge(birthyear) {
      let nowYear = new Date().getFullYear()
      let year = new Date(birthyear).getFullYear()
      return nowYear - year
    },

    // 当前页
    handleCurrentChange(val) {
      this.currentPage = val
    }
  },
  async created() {
    const { data: res } = await this.$axios.get('http://localhost:54418/api/station')
    if (res.status === 1) {
      this.options = res.item
      for (let i = 0; i < this.options.length; ++i) {
        const item = { value: i, label: this.options[i].line_name }
        this.line_options.push(item)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.getUserInfo()
    })
  },
  watch: {
    // 监听路线选择
    line_value(val) {
      if (val | (val === 0)) {
        this.station_value = ''
        this.station_options.splice(0, this.station_options.length)
        for (let i = 0; i < this.options.length; i++) {
          if (this.options[i].line_name === this.line_options[val].label) {
            for (let j = 0; j < this.options[i].sta.length; j++) {
              const item = { value: j, label: this.options[i].sta[j].sta_name }
              this.station_options.push(item)
            }
          }
        }
        this.is_disabled = false
        // 调用接口
      }
    }
  }
}
</script>
<style scoped>
#passengerinfo {
  width: 100%;
  height: 100%;
  padding: 30px;
  position: relative;
}
/* header部分 */
#header {
  width: 100%;
  height: 70px;
  margin-bottom: 15px;
}
#title {
  float: left;
  height: 100%;
  width: 30%;
}
#title > img {
  float: left;
  height: 90%;
  transform: translateY(5%);
  padding-left: 30px;
  padding-right: 20px;
}
#title > p {
  height: 100%;
  float: left;
  font-size: 31px;
  font-weight: bold;
  color: #143689;
  transform: translateY(22%);
  margin: 0px;
}
#select {
  padding-right: 80px;
  height: 100%;
  float: right;
  transform: translateY(25%);
}
/* table部分 */
#table {
  float: left;
  width: 38%;
  height: 90%;
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.16);
  padding: 10px 30px 10px;
  margin-right: 2%;
  display: flex;
  flex-flow: column;
  justify-content: space-between;
  align-items: center;
}
/* 图表部分 */
/* 暂时定高定宽，不然会出问题，后续再做修改 */
#chart {
  float: left;
  width: 900px;
  height: 630px;
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.16);
  margin-left: 2%;
  padding: 30px;
  padding-top: 20px;
}
</style>
