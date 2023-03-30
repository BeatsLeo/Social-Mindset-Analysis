function create_attitude_column(attitude_count) {
    console.log(attitude_count)

    //3.心态变化时间图（柱状图）
    var columnOption = {
        legend: {},
        tooltip: {},
        dataset: {},
        // 声明一个 X 轴，类目轴（category）。默认情况下，类目轴对应到 dataset 第一列。
        xAxis: {
            type: 'category',
            data:['高兴','搞笑', '期待', '肯定','感动', '悲伤', '愤怒', '厌恶', '担心', '无聊', '警惕', '惊讶', '无所谓'],
            axisLabel: {
                 interval:0,
                 rotate:40
            }
        },
        // 声明一个 Y 轴，数值轴。
        yAxis: {},
        // 声明多个 bar 系列，默认情况下，每个系列会自动对应到 dataset 的每一列。
        series: [
            {
                type: 'bar',
                data:Object.values(attitude_count),
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
            },
        ]
    };

    return columnOption;
}
        