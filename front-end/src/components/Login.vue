<template>
  <div id="login">
    <!-- 左侧图片 -->
    <div class="col-md-6">
      <img src="../assets/login_left.png" style="height: 100%;width: 100%;" />
      <div id="left_logo">
        <img src="../assets/logo.png" />
        <p>知客行</p>
      </div>
    </div>
    <!-- 右侧 -->
    <div class="col-md-6">
      <div id="right_top">
        <div id="logo">
          <img src="../assets/logo.png" />
          <p>登录</p>
        </div>
      </div>
      <!-- 右侧登录表单 -->
      <div id="right_bottom" style="height: 66%;">
        <div id="form_div">
          <form>
            <label>用户名:</label>
            <input
              type="text"
              class="form-control"
              placeholder="请输入用户名"
            />
            <label>密码:</label>
            <input
              type="password"
              class="form-control"
              placeholder="请输入密码"
            />
            <div id="button_div">
              <button type="button" @click="login">确认</button>
              <p>还没账号？<a href="">立刻注册</a></p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import '../lib/bootstrap/css/bootstrap.min.css'
export default {
  data() {
    return {}
  },
  methods: {
    login() {
      const tokenStr = 'test'
      window.sessionStorage.setItem('token', tokenStr)
      this.$router.push('/main')
    }
  }
}
</script>

<style scoped>
#login {
  position: fixed;
  width: 100%;
  height: 100%;
  background-color: #f3f7ff;
}
.col-md-6 {
  padding: 0;
  height: 100%;
}
/* 右上角区域 */
#right_top {
  height: 34%;
  position: relative;
}
#logo {
  width: 100%;
  position: absolute;
  bottom: 0;
  text-align: center;
}
#logo > img {
  width: 104px;
  height: 104px;
}
#logo > p {
  font-size: 49px;
  font-weight: bold;
  color: #143689;
}
/* 表单区域 */
#form_div {
  margin-left: 20%;
  margin-right: 20%;
  height: 80%;
}
label {
  height: 48px;
  font-size: 30px;
  font-weight: bold;
  line-height: 55px;
  color: #143689;
  opacity: 0.53;
}
input {
  height: 50px;
  font-size: 18px;
  border-radius: 8px;
}
#button_div {
  margin-top: 50px;
  width: 100%;
  text-align: center;
}
button {
  width: 243px;
  height: 67px;
  background-color: #467be5;
  border-radius: 13px;
  font-size: 33px;
  color: #ffffff;
  border: unset;
  outline: none;
}
button:hover,
button:active {
  background-color: #5bc0de;
}
#button_div > p {
  margin-top: 10px;
  color: #143689;
  font-size: 20px;
}
/* 左侧logo区 */
#left_logo {
  position: fixed;
  width: 321px;
  height: 104px;
  top: 8%;
  left: 5%;
}
#left_logo > img {
  width: 104px;
  height: 104px;
}
#left_logo > p {
  display: inline;
  padding-left: 30px;
  width: 183px;
  font-size: 60px;
  font-weight: bold;
  color: #ffffff;
  vertical-align: middle;
}
</style>
