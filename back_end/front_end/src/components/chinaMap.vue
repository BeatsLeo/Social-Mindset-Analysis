<template>
	<div ref="char" class="char"></div>
</template>

<script>
import * as echarts from 'echarts';
import china from '@/assets/china.json';
import ajax from "../axios";

echarts.registerMap('china', china);

export default {
  props: {
    attitude_color: Array,
  },
	data() {
      this.attitude_color=JSON.parse(JSON.stringify(this.attitude_color))
      return {
			// titledata: [],
			// resultdata0: [],
			// bartop6: [],

			yMax: 1000,
			// dataShadow: [],
			option: {
				title: [
					{
						show: false,
						text: '地域分布'
					}
				],
				tooltip: {
					trigger: 'item'
				},
				legend: {
					show: false
				},
				grid: {
					// 仅仅控制条形图的位置
					show: false,
					containLabel: false,
					top: 'center',
					right: 0,
					width: '20%',
					height: '40%'
				},
				// visualMap: {
				// 	type: 'continuous',
				// 	min: 0,
				// 	max: 1000,
				// 	text: ['多', '少'],
				// 	seriesIndex: [0, 2],
				// 	dimension: 0,
				// 	realtime: false,
				// 	left: 0,
				// 	orient: 'horizontal',
				// 	itemWidth: 11,
				// 	itemHeight: 143,
				// 	calculable: false,
				// 	inRange: {
				// 		color: ['#0C318B', '#3AB9FE'],
				// 		symbolSize: [100, 100]
				// 	},
				// 	outOfRange: {
				// 		color: ['#eeeeee'],
				// 		symbolSize: [100, 100]
				// 	},
				// 	textStyle: {}
				// },
				toolbox: {
					show: false
				},
				series: [
					{
						name: '心态分布',
						type: 'map',
						mapType: 'china',
						top: '10',
						left: 'center',
						width: '95%',
						roam: 'move',
						// mapValueCalculation: 'sum',
						zoom: 1,
						selectedMode: false,
						showLegendSymbol: false,
						label: {
							normal: {
								textStyle: {
									color: '#DBF8FF',
									fontSize: 10
								},
                formatter:'{c}',
								show: true
							},
							emphasis: {
								textStyle: {
									color: '#234EA5'
								}
							}
						},
						itemStyle: {
							normal: {
								areaColor: '#EEEEEE',
								borderColor: '#FFFFFF'
							},
							emphasis: {
								areaColor: '#E5F39B'
							}
						},
						data:[
                { name: '北京', selected: false, value: 1 },
                { name: '天津', selected: false, value: 2 },
                { name: '上海', selected: false, value: 3 },
                { name: '重庆', selected: false, value: 4 },
                { name: '河北', selected: false, value: 5 },
                { name: '河南', selected: false, value: 6 },
                { name: '云南', selected: false, value: 7 },
                { name: '辽宁', selected: false, value: 8 },
                { name: '黑龙江', selected: false, value: 9 },
                { name: '湖南', selected: false, value: 10 },
                { name: '安徽', selected: false, value: 11 },
                { name: '山东', selected: false, value: 12 },
                { name: '新疆', selected: false, value: 13 },
                { name: '江苏', selected: false, value: 14 },
                { name: '浙江', selected: false, value: 15 },
                { name: '江西', selected: false, value: 16 },
                { name: '湖北', selected: false, value: 17 },
                { name: '广西', selected: false, value: 18 },
                { name: '甘肃', selected: false, value: 19 },
                { name: '山西', selected: false, value: 20 },
                { name: '内蒙古', selected: false, value: 21 },
                { name: '陕西', selected: false, value: 22 },
                { name: '吉林', selected: false, value: 23 },
                { name: '福建', selected: false, value: 24 },
                { name: '贵州', selected: false, value: 25 },
                { name: '广东', selected: false, value: 26 },
                { name: '青海', selected: false, value: 27 },
                { name: '西藏', selected: false, value: 28 },
                { name: '四川', selected: false, value: 29 },
                { name: '宁夏', selected: false, value: 30 },
                { name: '海南', selected: false, value: 31 },
                { name: '台湾', selected: false, value: 32 },
                { name: '香港', selected: false, value: 33 },
                { name: '澳门', selected: false, value: 34 },
                { name: '南海诸岛', selected: false, value: 35 }
            ]
					}
				],
        dataRange: {
            x: '-1000 px', //图例横轴位置
            y: '-1000 px', //图例纵轴位置
            splitList: [
                { start: 1, end: 1, label: '北京', color: 'rgb('+this.attitude_color[0][0]+')' },
                { start: 2, end: 2, label: '天津', color: 'rgb('+this.attitude_color[1][1]+')' },
                { start: 3, end: 3, label: '上海', color: 'rgb('+this.attitude_color[2][2]+')' },
                { start: 4, end: 4, label: '重庆', color: 'rgb('+this.attitude_color[3][3]+')' },
                { start: 5, end: 5, label: '河北', color: 'rgb('+this.attitude_color[4][4]+')' },
                { start: 6, end: 6, label: '河南', color: 'rgb('+this.attitude_color[15][15]+')' },
                { start: 7, end: 7, label: '云南', color: 'rgb('+this.attitude_color[22][22]+')' },
                { start: 8, end: 8, label: '辽宁', color: 'rgb('+this.attitude_color[6][6]+')' },
                { start: 9, end: 9, label: '黑龙江', color: 'rgb('+this.attitude_color[8][8]+')' },
                { start: 10, end: 10, label: '湖南', color: 'rgb('+this.attitude_color[17][17]+')' },
                { start: 11, end: 11, label: '安徽', color: 'rgb('+this.attitude_color[11][11]+')' },
                { start: 12, end: 12, label: '山东', color: 'rgb('+this.attitude_color[14][14]+')' },
                { start: 13, end: 13, label: '新疆', color: 'rgb('+this.attitude_color[31][31]+')' },
                { start: 14, end: 14, label: '江苏', color: 'rgb('+this.attitude_color[9][9]+')' },
                { start: 15, end: 15, label: '浙江', color: 'rgb('+this.attitude_color[10][10]+')' },
                { start: 16, end: 16, label: '江西', color: 'rgb('+this.attitude_color[13][13]+')' },
                { start: 17, end: 17, label: '湖北', color: 'rgb('+this.attitude_color[16][16]+')' },
                { start: 18, end: 18, label: '广西', color: 'rgb('+this.attitude_color[28][28]+')' },
                { start: 19, end: 19, label: '甘肃', color: 'rgb('+this.attitude_color[24][24]+')' },
                { start: 20, end: 20, label: '山西', color: 'rgb('+this.attitude_color[5][5]+')' },
                { start: 21, end: 21, label: '内蒙古', color: 'rgb('+this.attitude_color[27][27]+')' },
                { start: 22, end: 22, label: '陕西', color: 'rgb('+this.attitude_color[23][23]+')' },
                { start: 23, end: 23, label: '吉林', color: 'rgb('+this.attitude_color[7][7]+')' },
                { start: 24, end: 24, label: '福建', color: 'rgb('+this.attitude_color[12][12]+')' },
                { start: 25, end: 25, label: '贵州', color: 'rgb('+this.attitude_color[21][21]+')' },
                { start: 26, end: 26, label: '广东', color: 'rgb('+this.attitude_color[18][18]+')' },
                { start: 27, end: 27, label: '青海', color: 'rgb('+this.attitude_color[25][25]+')' },
                { start: 28, end: 28, label: '西藏', color: 'rgb('+this.attitude_color[29][29]+')' },
                { start: 29, end: 29, label: '四川', color: 'rgb('+this.attitude_color[20][20]+')' },
                { start: 30, end: 30, label: '宁夏', color: 'rgb('+this.attitude_color[30][30]+')' },
                { start: 31, end: 31, label: '海南', color: 'rgb('+this.attitude_color[19][19]+')' },
                { start: 32, end: 32, label: '台湾', color: 'rgb('+this.attitude_color[16][16]+')' },
                { start: 33, end: 33, label: '香港', color: 'rgb('+this.attitude_color[32][32]+')' },
                { start: 34, end: 34, label: '澳门', color: 'rgb('+this.attitude_color[33][33]+')' },
                { start: 35, end: 35, label: '南海诸岛', color: 'rgb('+this.attitude_color[34][34]+')' }
            ]
        }, //各省地图颜色；start：值域开始值；end：值域结束值；label：图例名称；color：自定义颜色值；
			}
		};

	},
	methods: {
    init() {
      this.myChart = echarts.init(this.$refs.char);
      this.myChart.setOption(this.option);
    },
  },
	mounted() {
		this.init();
	},
	created() {
		// this.init2();
	},
	watch: {
		// titledata(value) {
		// 	this.option.yAxis[0].data = value;
		// 	this.myChart.setOption(this.option);
		// },
		// citydata(value) {
		// 	this.option.series[0].data = value;
		// 	this.myChart.setOption(this.option);
		// },
		// dataShadow(value) {
		// 	this.option.series[1].data = value;
		// 	this.myChart.setOption(this.option);
		// },
		// bartop6(value) {
		// 	this.option.series[2].data = value;
		// 	this.myChart.setOption(this.option);
		// }
	}
};
</script>

<style lang="less" scoped>
.char {
	width: 100%;
	height: 100%;
}
</style>
