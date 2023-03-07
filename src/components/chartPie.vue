<template>
	<div ref="chartPie" class="chartPie"></div>
</template>
 
<script>
import echarts from 'echarts';

export default {
  props: {
    chartPieData: Object,
  },
	data() {
		return {
			option: {
        color: ['#B4C7E7', '#A6AFB6', '#496A9F', '#26426F', '#0D141F'],
        tooltip:{
            trigger:"item"
        },
        series: [
          {
            // color: '#8E9CBD',
            type: "pie",  // 类型 饼图
            // radius: [50, 250], // 饼图的半径 `50, 250 => 内半径 外半径`
            center: ["50%", "50%"], // 饼图的中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标。
            // roseType: "area", // 是否展示成南丁格尔图，通过半径区分数据大小
            // 图形的颜色
            itemStyle: {
              borderRadius: 8,
            },
            textStyle: {                 // 词典样式配置
                normal: {
                  color(v) {
                    // 颜色随机渐变
                    let colors = ['#B4C7E7', '#A6AFB6', '#496A9F', '#26426F', '#0D141F']
                    return colors[v.data.level]
                  }
                }
              },
            data: this.chartPieData,
          }
        ]
      }
		};
	},
	methods: {
		init() {
      // 获取到ref绑定为loginTimes的DOM节点，以canvas的形式展现在视图层
      let myChart = echarts.init(this.$refs.chartPie)
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
.chartPie {
  width: 100%;
  height: 100%;
}
</style>