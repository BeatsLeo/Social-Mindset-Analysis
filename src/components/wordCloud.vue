<template>
	<div ref="wordcloud" class="wordcloud"></div>
</template>
 
<script>
import echarts from 'echarts';
import 'echarts-wordcloud';

export default {
  props: {
    worddata: Array,

  },
	data() {
		return {
			option: {
          backgroundColor: '#E5EAF1', // canvas背景颜色
          // canvas标题配置项
          title: {
            // text: '我是标题',
            top: '0%',
            left: '-1%',
            textStyle: {
                fontSize: 14,
                color: '#3B3E41',
                fontWeight: 'normal'
            }
          },
          tooltip: {
            trigger: 'item'
          },
          series: [
            {
              type: 'wordCloud',
              left: '0%',    
              right: '0%',              
              top: '5%',                  // Y轴偏移量
              width: '100%',               // canvas宽度大小
              height: '100%',              // canvas高度大小
              sizeRange: [12, 40],         //  词典字体大小范围配置
              rotationRange: [0, 0],       // 词典字体旋转角度配置，默认不旋转
              gridSize: 20,                // 词典字体间距配置
              layoutAnimation: true,       // 为false词典过度会阻塞
              textStyle: {                 // 词典样式配置
                normal: {
                  color(v) {
                    // 颜色随机渐变
                    let colors = ['#B4C7E7', '#A6AFB6', '#496A9F', '#26426F', '#0D141F']
                    return colors[v.data.level]
                  }
                }
              },
              // 渲染词典数据
              data: this.worddata
            }
          ]
      }
		};
	},
	methods: {
		initwordCloud() {
      // 处理数据
      this.worddata.sort(function(a, b){
          return a.value - b.value
      })
      const l = this.worddata.length;
      this.worddata.forEach((item, index) => {
        var i = (index+1) / l;
        var level = 0;
        if(i > 0.8){
          level = 4;
        }else if(i > 0.6){
          level = 3;
        }else if(i > 0.4){
          level = 2;
        }else if(i > 0.2){
          level = 1;
        }else if(i > 0){
          level = 0;
        }
        item.level = level;
      })

      // 获取到ref绑定为loginTimes的DOM节点，以canvas的形式展现在视图层
      let myChart = echarts.init(this.$refs.wordcloud)
      // echarts参数设置
      myChart.setOption(this.option)
    }
	},
	mounted() {
		this.initwordCloud();
	},
	created() {
	},
	watch: {
	}
};
</script>
 
<style lang="less" scoped>
.wordcloud {
  width: 100%;
  height: 100%;
}
</style>