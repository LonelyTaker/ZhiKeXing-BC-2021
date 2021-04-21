<template>
  <div style="width:100%;height:100%">
    <img src="@/assets/fictitious/live_map.png" style="width:100%;height:100%" v-if="flag" @click="select" />
    <img src="@/assets/fictitious/heat.png" style="width:100%;height:100%" v-if="!flag" @click="select" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      flag: true
    }
  },
  methods: {
    select() {
      this.flag = !this.flag
    }
  }
}
</script>
