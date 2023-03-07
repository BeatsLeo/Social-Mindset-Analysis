function create_attitude_wordcloud() {
    const wordcloudOpttion = () => {
       const data = [
                        {"name":"男神","value":2.64},
                        {"name":"好身材","value":4.03},
                        {"name":"校草","value":24.95},
                        {"name":"酷","value":4.04},
                        {"name":"时尚","value":5.27},
                        {"name":"阳光活力","value":5.80},
                        {"name":"初恋","value":3.09},
                        {"name":"英俊潇洒","value":24.71},
                        {"name":"霸气","value":6.33},
                        {"name":"腼腆","value":2.55},
                        {"name":"蠢萌","value":3.88},
                        {"name":"青春","value":8.04},
                        {"name":"网红","value":5.87},
                        {"name":"萌","value":6.97},
                        {"name":"认真","value":2.53},
                        {"name":"古典","value":2.49},
                        {"name":"温柔","value":3.91},
                        {"name":"有个性","value":3.25},
                        {"name":"可爱","value":9.93},
                        {"name":"幽默诙谐","value":3.65}
      ];

      const nums = data.map((item) => item.value);
      const min = Math.min(...nums);
      const max = Math.max(...nums);
      const color = [
          'rgb(13,20,31)',
          'rgb(38,66,111)',
          'rgb(73,106,159)',
          'rgb(166,175,182)',
          'rgb(255,242,204)',
      ];

      return {
         visualMap: {
          type: 'piecewise',
          show: false, // 如果设置为 false，不会显示，但是数据映射的功能还存在
          min,
          max,
          splitNumber: 5, // 5个颜色，所以分成5段
          color
        },
        series: [
          {
            type: 'wordCloud',
            shape: 'square',
            sizeRange:[15, 80],
            drawOutOfBound: true, // 默认超出不显示
            // textStyle: {
            //   color: function(e) {
            //     return color[e.dataIndex % 6];
            //   }
            // },
            data
          }
        ]
      };
    };

    return wordcloudOpttion()
}
