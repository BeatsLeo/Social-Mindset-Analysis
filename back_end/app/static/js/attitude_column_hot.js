function create_attitude_column(hot_count) {
    console.log(hot_count)
    var province=[]
    var hot=[]
    for(var i=0;i<10;i++){
        province[i]=Object.keys(hot_count)[i]
        hot[i]=Object.values(hot_count)[i]
    }
    //3.心态变化时间图（柱状图）
    var columnOption = {
        legend: {},
        tooltip: {},
        dataset: {},
        // 声明一个 X 轴，类目轴（category）。默认情况下，类目轴对应到 dataset 第一列。
        xAxis: {
            type: 'category',
            data:province,
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
                data:hot,
                itemStyle: {
                    barBorderRadius: [2, 2, 0, 0], //柱体圆角
                    color: new echarts.graphic.LinearGradient(
                        //前四个参数用于配置渐变色的起止位置，这四个参数依次对应 右下左上 四个方位。也就是从右边开始顺时针方向。
                        //通过修改前4个参数，可以实现不同的渐变方向
                        /*第五个参数则是一个数组，用于配置颜色的渐变过程。
                          每项为一个对象，包含offset和color两个参数
                        */
                        0, 0, 0, 1, [{//代表渐变色从正上方开始
                                offset: 0, //offset范围是0~1，用于表示位置，0是指0%处的颜色
                                color: 'rgb(90,126,192)'
                            }, //柱图渐变色
                            {
                                offset: 1, //指100%处的颜色
                                color: 'rgb(227,233,241)'
                            }
                        ]
                    ),
                }
            },
        ]
    };

    return columnOption;
}
        