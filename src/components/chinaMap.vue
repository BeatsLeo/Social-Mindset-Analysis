<template>
	<div ref="char" class="char"></div>
</template>
 
<script>
import * as echarts from 'echarts';
import china from '@/assets/china.json';

echarts.registerMap('china', china);

export default {
  props: {
    citydata: Array,
  },
	data() {
		return {
			titledata: [],
			resultdata0: [],
			bartop6: [],
			yMax: 1000,
			dataShadow: [],
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
				visualMap: {
					type: 'continuous',
					min: 0,
					max: 1000,
					text: ['多', '少'],
					seriesIndex: [0, 2],
					dimension: 0,
					realtime: false,
					left: 0,
					orient: 'horizontal',
					itemWidth: 11,
					itemHeight: 143,
					calculable: false,
					inRange: {
						color: ['#0C318B', '#3AB9FE'],
						symbolSize: [100, 100]
					},
					outOfRange: {
						color: ['#eeeeee'],
						symbolSize: [100, 100]
					},
					textStyle: {}
				},
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
						mapValueCalculation: 'sum',
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
						data: this.citydata
					}
				]
			}
		};
	},
	methods: {
		init() {
			this.myChart = echarts.init(this.$refs.char);
			this.myChart.setOption(this.option);
		},
		init2() {
			this.citydata.sort((a, b) => {
				return b.value - a.value;
			});
			for (var i = 0; i < 6; i++) {
				var top10 = {
					name: this.citydata[i].name,
					value: this.citydata[i].value
				};
				this.bartop6.push(top10);
				this.dataShadow.push(this.yMax);
			}
			this.bartop6.sort((a, b) => {
				return a.value - b.value;
			});
			for (var i = 0; i < this.bartop6.length; i++) {
				this.titledata.push(this.bartop6[i].name);
			}
		}
	},
	mounted() {
		this.init();
	},
	created() {
		this.init2();
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