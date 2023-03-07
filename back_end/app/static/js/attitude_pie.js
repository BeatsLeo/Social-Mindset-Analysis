function create_attitude_pie(attitude_count) {
    console.log(attitude_count)
    //2.心态变化时间图（饼图）
    var pieOption ={
        series : [{
                name: '测试报告',
                type: 'pie',    // 设置图表类型为饼图
                radius: '55%',  // 饼图的半径，外半径为可视区尺寸（容器高宽中较小一项）的 55% 长度。
                label: {
                    position: 'outside',
                    formatter: '{b}:{c} ({d}%)'
                },
                data:[          // 数据数组，name 为数据项名称，value 为数据项值
                    {name:'高兴', value: attitude_count[0]},
                    {name:'搞笑', value:attitude_count[1]},
                    {name:'期待', value:attitude_count[2]},
                    {name:'肯定', value:attitude_count[3]},
                    {name:'感动', value:attitude_count[4]},
                    {name:'悲伤', value:attitude_count[5]},
                    {name:'愤怒', value:attitude_count[6]},
                    {name:'厌恶', value:attitude_count[7]},
                    {name:'担心', value:attitude_count[8]},
                    {name:'无聊', value:attitude_count[9]},
                    {name:'警惕', value:attitude_count[10]},
                    {name:'惊讶', value:attitude_count[11]},
                    {name:'无所谓', value:attitude_count[12]},
                ],
                // 此系列自己的调色盘
                color: ['#FFF2CC', '#FFE699', '#FFD966', '#FFBD0B', '#F2B100', '#CBD3EA', '#9DACD5', '#6379B5', '#2B458F', '#021750', '#E2F0D9', '#C5E0B4', '#A9D18E']
        }
        ]
    }

    return pieOption;
}