<template>
	<div ref="chartCategory" class="chartCategory"></div>
</template>

<script>
import echarts from 'echarts';

export default {
  props: {
    attitude_count: Array,
  },
	data() {
    // this.attitude_count=JSON.parse(JSON.stringify(this.attitude_count))
    var hot=[]
    for(var i=0;i<13;i++){
        hot[i]=this.attitude_count[i][i]
    }
    console.log(hot)
		return {
			option: {
        tooltip:{
            trigger:"item"
        },
        xAxis: {
          type: 'category',
          data:['高兴','搞笑', '期待', '肯定','感动', '悲伤', '愤怒', '厌恶', '担心', '无聊', '警惕', '惊讶', '无所谓'],
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
            itemStyle: {
            normal: {
　　　　　　　　//这里是重点
                color: function(params) {
                	//注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
                    var colorList = [ '#FFF2CC', '#FFE699',  '#FFD966', '#FFBD0B', '#F2B100', '#CBD3EA', '#9DACD5', '#6379B5', '#2B458F', '#021750', '#E2F0D9', '#C5E0B4', '#A9D18E'];
                    return colorList[params.dataIndex]
                }
            }
        }
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
