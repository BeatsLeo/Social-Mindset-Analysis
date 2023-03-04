<template>
	<div ref="chartCategory" class="chartCategory"></div>
</template>

<script>
import echarts from 'echarts';

export default {
  props: {
    hot_count: Object,
  },
	data() {
    this.hot_count=JSON.parse(JSON.stringify(this.hot_count))
    var data=JSON.parse(JSON.stringify(Object.values(this.hot_count)))
    data=Object.values(data)
    var province=[]
    var hot=[]
    for(var i=0;i<10;i++){
        province[i]=Object.keys(data[i])[0]
        hot[i]=Object.values(data[i])[0]
    }
    province=JSON.parse(JSON.stringify(province))
    hot=JSON.parse(JSON.stringify(hot))
		return {
			option: {
        tooltip:{
            trigger:"item"
        },
        xAxis: {
          type: 'category',
          data: province,
          axisLabel: {
                 interval:0,
                 rotate:40
            }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: hot,
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
