<template>
  <div id="main">
    <el-container>
      <!-- 模块导航栏 -->
      <el-aside width="185px" style="position: relative">
        <!-- logo -->
        <div style="width:100%;text-align: center;padding-top:30px;padding-bottom:30px">
          <img src="../assets/logo.png" style="width:107px;height:107px;" />
        </div>
        <!-- 导航栏 -->
        <div style="width:100%;text-align: center;">
          <el-button type="primary" icon="el-icon-live" @click="live_btn_click">地铁实况</el-button>
          <el-button type="primary" icon="el-icon-forecast" @click="forecast_btn_click">客流预测</el-button>
          <el-button type="primary" icon="el-icon-history" @click="history_btn_click">数据分析</el-button>
        </div>
        <!-- 底部设置和帮助 -->
        <div style="width:100%;text-align: center;height:150px;position: absolute;bottom: 0;">
          <el-button type="primary" icon="el-icon-setting" style="margin:5px;width:90%;height:50px;border-radius: 10px;font-size:24px">设置</el-button>
          <el-button type="primary" icon="el-icon-info" style="margin:5px;width:90%;height:50px;border-radius: 10px;font-size:24px">帮助</el-button>
        </div>
      </el-aside>
      <el-container>
        <!-- header -->
        <el-header height="100px">
          <p>{{ modular_title }}</p>
          <div id="message">
            <a href="#"><img src="../assets/message.png"/></a>
            <a href="#"><img src="../assets/work.png"/></a>
            <a href="#">
              <img src="../assets/user.png" class="img-rounded" style="width:70px;height:70px" />
            </a>
            <a href="#"><img src="../assets/select.png" style="width:30px;height:30px;margin: 3px;"/></a>
          </div>
          <div id="weather">
            <p>{{ weather_info }}</p>
            <p>{{ temperature }}℃</p>
          </div>
          <div class="input-group" id="search-input">
            <div class="input-group-addon"><i class="el-icon-search"></i></div>
            <input type="text" class="form-control" id="exampleInputAmount" placeholder="输入关键词搜索" />
          </div>
        </el-header>
        <!-- main -->
        <div :class="flag == 1 ? 'notice1' : 'notice2'">
          <div style="height:100%;width:500px;display:flex;align-items: center;">
            <a id="noticeText">{{ notice }}</a>
          </div>
          <img src="../assets/train.png" style="width:30px;height:20px" />
        </div>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<script>
export default {
  data() {
    return {
      modular_title: '',
      weather_info: '未知',
      temperature: '--',
      flag: 0,
      notice: '10号线(Sta145-162 上行) 1025次列车故障停车  '
    }
  },
  methods: {
    live_btn_click() {
      this.$router.push('/main/live')
      this.modular_title = '地铁实况'
      this.flag = 0
    },
    forecast_btn_click() {
      this.$router.push('/main/forecast')
      this.modular_title = '客流预测'
      this.flag = 0
    },
    history_btn_click() {
      this.$router.push('/main/history')
      this.modular_title = '数据分析'
      this.flag = 1
    },
    noticeGo() {
      var start = this.notice.substring(0, 1)
      var end = this.notice.substring(1)
      this.notice = end + start
    }
  },
  // 利用高德api，获取天气信息
  /* eslint-disable */
  async created() {
    const { data: res } = await this.$axios.get('https://restapi.amap.com/v3/weather/weatherInfo?city=110101&key=	665d78b7d3011217163feb16eb54420f')
    if (res.status == 1) {
      this.weather_info = res.lives[0].weather
      this.temperature = res.lives[0].temperature
    }
  },
  // 刷新后的页面
  mounted() {
    if ((this.$route.path === '/main/live/map') | (this.$route.path === '/main/live/line') | (this.$route.path === '/main/live/sta')) {
      this.modular_title = '地铁实况'
    } else if (this.$route.path === '/main/forecast') {
      this.modular_title = '客流预测'
    } else {
      this.flag = 1
      this.modular_title = '数据分析'
    }
    setInterval(this.noticeGo, 200)
  }
}
</script>
<style scoped>
#main {
  height: 100%;
  background: #f3f7ff;
}
.el-container {
  height: 100%;
}
.el-aside {
  background-color: #7698ff;
}
/* 改变element-ui预设的按钮样式 */
.el-button--primary.is-active,
.el-button--primary:active {
  background: #7698ff;
  border-color: #7698ff;
  color: #fff;
}
.el-button--primary:focus,
.el-button--primary:hover {
  background: #96a6ff;
  border-color: #96a6ff;
  color: #fff;
}
.el-button--primary {
  color: #fff;
  background-color: #7698ff;
  border-color: #7698ff;
  margin: 5px;

  width: 90%;
  height: 50px;
  border-radius: 10px;
  font-size: 24px;
}
/* header */
.el-header {
  line-height: 100px;
  padding-right: 40px;
  padding-left: 40px;
}
.el-header > p {
  width: 200px;
  font-size: 40px;
  font-weight: bold;
  color: #143689;
  margin: 0px;
  float: left;
}
#weather {
  float: right;
  height: 74px;
  width: 150px;
  background-color: white;
  transform: translateY(13px);
  border-radius: 12px;
  margin-right: 15px;
  text-align: center;
}
#weather > p {
  line-height: 37px;
  height: 37px;
  margin: 0px;
  font-size: 20px;
  font-weight: bold;
  color: #505ed0;
}
#message {
  float: right;
  height: 100%;
  width: 300px;
}
#message > a > img {
  margin: 10px;
  width: 40px;
  height: 40px;
}
#search-input {
  width: 40%;
  height: 50%;
  float: right;
  transform: translateY(24px);
  margin-right: 30px;
}
#search-input > input {
  height: 100%;
  font-size: 20px;
}
/* main */
.el-main {
  padding: 40px;
  padding-top: 0px;
  padding-bottom: 20px;
}
/* 公告部分 */
.notice1 {
  position: absolute;
  right: 40px;
  top: 100px;
  width: 1000px;
  height: 40px;
  display: flex;
  align-items: center;
  flex-direction: row-reverse;
}
.notice2 {
  position: absolute;
  right: 40px;
  top: 100px;
  width: 1000px;
  height: 80px;
  display: flex;
  align-items: center;
  flex-direction: row-reverse;
}
#noticeText {
  padding: 0 10px 0;
  margin: 0;
  font: 400 18px sans-serif;
  color: #143689;
  opacity: 0.8;
}
</style>
