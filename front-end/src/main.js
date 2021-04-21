import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/font_icon/iconfont.css'
import axios from 'axios'
import * as echarts from 'echarts'
Vue.prototype.$echarts = echarts
Vue.prototype.$axios = axios

Vue.use(ElementUI)
Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
