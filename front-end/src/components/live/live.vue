<template>
  <div id="live">
    <div id="header">
      <div id="select">
        <el-select v-model="line_value" placeholder="请选择站线" clearable @clear="reselect">
          <el-option v-for="line_item in line_options" :key="line_item.value" :label="line_item.label" :value="line_item.value"> </el-option>
        </el-select>
        <el-select v-model="station_value" placeholder="请选择站点" :disabled="is_disabled" @change="go_live_sta">
          <el-option v-for="station_item in station_options" :key="station_item.value" :label="station_item.label" :value="station_item.value"> </el-option>
        </el-select>
      </div>
    </div>
    <div id="main">
      <router-view></router-view>
    </div>
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
      is_disabled: true
    }
  },
  methods: {
    reselect() {
      this.is_disabled = true
      this.station_value = ''
      this.line_value = ''
      this.$router.push('/main/live/map')
    },
    go_live_sta() {
      this.$router.push('/main/live/sta')
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
  watch: {
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
        this.$router.push('/main/live/line')
      }
    }
  }
}
</script>
<style scoped>
#live {
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
