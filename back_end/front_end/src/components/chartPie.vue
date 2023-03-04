<template>
	<div ref="chartPie" class="chartPie"></div>
</template>

<script>
import echarts from 'echarts';

export default {
  props: {
    attitude_count: Object,
  },
	data() {
    this.attitude_count=JSON.parse(JSON.stringify(this.attitude_count))
		return {
			option: {
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
            // textStyle: {                 // 词典样式配置
            //     normal: {
            //       color(v) {
            //         // 颜色随机渐变
            //         let colors = ['#B4C7E7', '#A6AFB6', '#496A9F', '#26426F', '#0D141F']
            //         return colors[v.data.level]
            //       }
            //     }
            //   },
            data:[          // 数据数组，name 为数据项名称，value 为数据项值
                    {name:'高兴', value: this.attitude_count[0][0]},
                    {name:'搞笑', value:this.attitude_count[1][1]},
                    {name:'期待', value:this.attitude_count[2][2]},
                    {name:'肯定', value:this.attitude_count[3][3]},
                    {name:'感动', value:this.attitude_count[4][4]},
                    {name:'悲伤', value:this.attitude_count[5][5]},
                    {name:'愤怒', value:this.attitude_count[6][6]},
                    {name:'厌恶', value:this.attitude_count[7][7]},
                    {name:'担心', value:this.attitude_count[8][8]},
                    {name:'无聊', value:this.attitude_count[9][9]},
                    {name:'警惕', value:this.attitude_count[10][10]},
                    {name:'惊讶', value:this.attitude_count[11][11]},
                    {name:'无所谓', value:this.attitude_count[12][12]},
                ],
            color: ['#FFF2CC', '#FFE699', '#FFD966', '#FFBD0B', '#F2B100', '#CBD3EA', '#9DACD5', '#6379B5', '#2B458F', '#021750', '#E2F0D9', '#C5E0B4', '#A9D18E']
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
