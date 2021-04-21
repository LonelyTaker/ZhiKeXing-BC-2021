import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login.vue'
import Main from '../components/Main.vue'
import Live from '../components/live/live.vue'
import History from '../components/history/history.vue'
import Forecast from '../components/forecast/forecast.vue'
import LiveMap from '../components/live/submodule/map.vue'
import LiveLine from '../components/live/submodule/line.vue'
import LiveSta from '../components/live/submodule/sta.vue'
Vue.use(Router)
const router = new Router({
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/main',
      component: Main,
      redirect: '/main/live/map',
      children: [
        {
          path: '/main/live',
          component: Live,
          redirect: '/main/live/map',
          children: [
            { path: '/main/live/map', component: LiveMap },
            { path: '/main/live/line', component: LiveLine },
            { path: '/main/live/sta', component: LiveSta }
          ]
        },
        {
          path: '/main/forecast',
          component: Forecast
        },
        {
          path: '/main/history',
          component: History
        }
      ]
    }
  ]
})
router.beforeEach((to, from, next) => {
  if (to.path === '/login') {
    return next()
  } else {
    const tokenStr = window.sessionStorage.getItem('token')
    if (!tokenStr) {
      return next('/login')
    } else {
      return next()
    }
  }
})

export default router
