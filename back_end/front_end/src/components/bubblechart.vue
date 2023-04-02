<template>
  <div>
    <canvas id="myCanvas" width="400" height="600"></canvas>
    <div id="out" style="float: right"></div>
  </div>
</template>

<script>
export default {
  name: "BubbleChart",
  data() {
    return {
      circles: [
        {
          color: "red",
          sense: "快乐",
          score: "100",
        },
        {
          color: "orange",
          sense: "难过",
          score: "20",
        },
        {
          color: "yellow",
          sense: "中立",
          score: "80",
        },
        {
          color: "green",
          sense: "感动",
          score: "100",
        },
        {
          color: "blue",
          sense: "失望",
          score: "20",
        },
        {
          color: "purple",
          sense: "愤怒",
          score: "80",
        },
        {
          sense: "愤怒",
          color: "black",
          score: "80",
        },
      ],
    };
  },
  methods: {},
  mounted() {
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    let circles = this.circles;
    function handleData() {
      for (let i = 0; i < circles.length; i++) {
        circles[i].curr = 0;
        circles[i].radius = parseInt(circles[i].score) / 1.1;
      }
      for (let i = 0; i < circles.length; i++) {
        let tag = true;
        let radius = circles[i].radius;
        let x = Math.random() * width;
        let y = Math.random() * height;
        for (let j = 0; j < i; j++) {
          let lx = circles[j].x;
          let ly = circles[j].y;
          let lradius = circles[j].radius;
          if (
            (x - lx) * (x - lx) + (y - ly) * (y - ly) <
            (radius + lradius) * (radius + lradius)
          ) {
            tag = false;
          }
        }
        if (x < radius || width - x < radius) {
          tag = false;
        }
        if (y < radius || height - y < radius) {
          tag = false;
        }
        if (tag === false) {
          tag = true;
          i--;
        } else {
          circles[i].x = x;
          circles[i].y = y;
        }
      }
    }
    handleData();
    //获取canvas文字的长度
    function getTextWidth(text, font) {
      // 重用canvas对象以获得更好的性能
      // re-use canvas object for better performance
      var canvas =
        getTextWidth.canvas ||
        (getTextWidth.canvas = document.createElement("canvas"));
      var context = canvas.getContext("2d");
      // console.log('context=', context) 获得对绘图上下文canvas的引用
      context.font = font;
      var metrics = context.measureText(text);
      return metrics.width;
    }
    //监听鼠标移动
    canvas.addEventListener("mousemove", function (e) {
      var rect = canvas.getBoundingClientRect(); // 获取画布的矩形区域
      var mouseX = e.clientX - rect.left; // 计算鼠标相对于画布左上角的坐标
      var mouseY = e.clientY - rect.top;

      for (var i = 0; i < circles.length; i++) {
        var circle = circles[i];
        var dx = mouseX - circle.x; // 计算鼠标与圆心的距离
        var dy = mouseY - circle.y;
        var distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < circle.radius) {
          // 如果鼠标在圆内，则修改鼠标样式为手型，并放大该圆
          canvas.style.cursor = "pointer";
          return;
        }
      }
      canvas.style.cursor = "default"; // 否则恢复鼠标样式为箭头，不放大圆
    });
    //监听鼠标单击
    canvas.addEventListener("click", function (e) {
      var rect = canvas.getBoundingClientRect(); // 获取画布的矩形区域
      var mouseX = e.clientX - rect.left; // 计算鼠标相对于画布左上角的坐标
      var mouseY = e.clientY - rect.top;

      for (var i = 0; i < circles.length; i++) {
        var circle = circles[i];
        var dx = mouseX - circle.x; // 计算鼠标与圆心的距离
        var dy = mouseY - circle.y;
        var distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < circle.radius) {
          // 如果鼠标在圆内，则修改鼠标样式为手型，并放大该圆
          document.getElementById(
            "out"
          ).innerHTML = `<h1>我选择了${circle.sense}</h1>`;
          return;
        }
      }
    });
    //画所有圆
    function drawCircle(ctx, x, y, radius, color, sense) {
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, 2 * Math.PI);
      var canvasGradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
      canvasGradient.addColorStop(0, "white");
      canvasGradient.addColorStop(1, color);
      ctx.fillStyle = canvasGradient;
      ctx.fill();
      // 设置文本样式
      ctx.font = `${radius / 3}px Arial`;
      ctx.fillStyle = "#000000";
      ctx.strokeStyle = "#0000ff";
      // 填充文本
      ctx.fillText(sense, x - getTextWidth(sense, ctx.font) / 2, y);
    }
    function drawCircles(ctx, circles) {
      ctx.clearRect(0, 0, canvas.width, canvas.height); // 清空画布
      for (var i = 0; i < circles.length; i++) {
        var circle = circles[i];
        drawCircle(
          ctx,
          circle.x,
          circle.y,
          circle.curr,
          circle.color,
          circle.sense
        );
        circles[i].curr += (circles[i].radius - circles[i].curr) / 50;
      }
    }

    //入口渲染函数
    function draw() {
      drawCircles(ctx, circles);
      requestAnimationFrame(draw);
    }
    draw();
  },
};
</script>

<style>
canvas {
  border: 1px solid white;
  cursor: default;
  /* 设置默认鼠标样式为箭头 */
}
</style>