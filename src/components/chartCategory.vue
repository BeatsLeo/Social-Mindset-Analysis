<template>
	<div ref="chartCategory" class="chartCategory"></div>
</template>
 
<script>
import echarts from 'echarts';

export default {
  props: {
    chartCategoryData: Object,
  },
	data() {
		return {
			option: {
        tooltip:{
            trigger:"item"
        },
        xAxis: {
          type: 'category',
          data: this.chartCategoryData.name
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: this.chartCategoryData.value,
            type: 'bar',
            color: '#8E9CBD',
          }
        ]
      }
		};
	},
	methods: {
		init() {
      // 获取到ref绑定为loginTimes的DOM节点，以canvas的形式展现在视图层
      let myChart = echarts.init(this.$refs.chartCategory)
      // echarts参数设置
      myChart.setOption(this.option)
    }
	},
	mounted() {
		this.init();
	},
	created() {
	},
	watch: {
	}
};
</script>
 
<style lang="less" scoped>
.chartCategory {
  width: 100%;
  height: 100%;
}
</style>