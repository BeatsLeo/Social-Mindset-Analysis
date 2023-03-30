<template>
  <div ref="chart" :style="{ width: '100%', height: '400px' }"></div>
</template>

<script>
import echarts from 'echarts'

export default {
  name: 'chartLine',
  props: {
    data: {
      type: Array,
      required: true
    }
  },
  mounted() {
    this.initChart()
  },
  methods: {
    initChart() {
      const chartDom = this.$refs.chart
      const myChart = echarts.init(chartDom)
      const option = {
        xAxis: {
          type: 'category',
          data: this.data.map(item => item.time)
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: this.data.map(item => item.value),
          type: 'line'
        }]
      }
      myChart.setOption(option)
    }
  }
}
</script>