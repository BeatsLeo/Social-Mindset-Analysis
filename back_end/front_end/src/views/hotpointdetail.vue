<template>
  <div class="hotpointdetailView" v-if="ShowPage">
    <el-col :span="11">
      <h2><i class="el-icon-s-opportunity"></i>&nbsp;事件详情</h2>
      <el-divider></el-divider>
      <el-row>
        <div class="h3div">
          <h3>事件背后原数据</h3>
        </div>
        <el-card class="box-card">
          <span>
            {{content}}
          </span>
        </el-card>
      </el-row>
      <br>
      <el-row>
        <div class="h3div">
          <h3>评论词云</h3>
        </div>
        <div class="wordcloud">
          <word-cloud :worddata="wordData"></word-cloud>
        </div>
      </el-row>
    </el-col>

    <el-col :span="2">&nbsp;</el-col>

    <el-col :span="11">
      <el-row>
        <div class="h3div">
          <h3>心态分布图</h3>
        </div>
        <el-row class="maprow">
          <div class="map" >
            <china-map :attitude_color="mapData"></china-map>
          </div>
        </el-row>
        <el-row>
          <el-col :span="12">
            <div class="chartCategory">
              <chart-category :attitude_count="chartCategoryData"></chart-category>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chartPie" >
              <chart-pie :attitude_count="chartPieData"></chart-pie>
            </div>
          </el-col>
        </el-row>
      </el-row>
    </el-col>
  </div>
</template>

<script>
import ajax from '../axios';
import wordCloud from '@/components/wordCloud.vue';
import ChinaMap from '@/components/chinaMap.vue';
import ChartCategory from '@/components/chartCategory_attitude.vue';
import ChartPie from '@/components/chartPie.vue';

export default {
  data () {
    return {
      content: "",
      wordData:[],
      mapData:[],
      chartCategoryData:[],
      chartPieData:[],
      ShowPage:false,
      flag_map:false,
      flag_pie_column:false,
      flag_word_cloud:false,
    }
  },
  components: {
    wordCloud,
    ChinaMap,
    ChartCategory,
    ChartPie,
  },
  mounted() {
    this.init();
  },
  methods: {
    init(){
      this.content = this.$route.query.content;
      this.id=this.$route.query.id;

      ajax({
        url: 'http://127.0.0.1:8000/api/rdsj/attitude_map/',
        method: 'get',
        params: {
          id:this.id,
        }
      })
        .then((data) => {
          console.log("attitude_map:",JSON.parse(JSON.stringify(data)))
          this.mapData=JSON.parse(JSON.stringify(data));
          this.flag_map=true;
          if(this.flag_pie_column&&this.flag_word_cloud){
            this.ShowPage = true;
          }
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
      ajax({
        url: 'http://127.0.0.1:8000/api/rdsj/attitude_pie_column/',
        method: 'get',
        params: {
          id:this.id,
        }
      })
        .then((data) => {
          console.log("attitude_pie_column:",JSON.parse(JSON.stringify(data)))
          this.chartPieData=JSON.parse(JSON.stringify(data));
          this.chartCategoryData=JSON.parse(JSON.stringify(data));
          this.flag_pie_column=true;
          if(this.flag_map&&this.flag_word_cloud){
            this.ShowPage = true;
          }
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
      ajax({
        url: 'http://127.0.0.1:8000/api/rdsj/comment_cloud/',
        method: 'get',
        params: {
          id:this.id,
        }
      })
        .then((data) => {
          console.log("comment_cloud:",JSON.parse(JSON.stringify(data)))
          this.wordData=JSON.parse(JSON.stringify(data));
          this.flag_word_cloud=true;
          if(this.flag_map&&this.flag_column){
            this.ShowPage = true;
          }
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
    },
  }
}
</script>

<style lang="less">
.hotpointdetailView{
  width:100%;
  height:100%;

  h2 {
    font-size: 16px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin-block-start: 10px;
    margin-block-end: 10px;
    margin-left: 10px;
  }

  .h3div{
    display: flex;
    justify-content: flex-start;
    align-items: center;

    h3 {
      font-size: 14px;
      display: flex;
      justify-content: flex-start;
      align-items: center;
      margin-block-start: 4px;
      margin-block-end: 4px;
      // color: #fff;
      background: #afc1f1;
      padding: 6px 24px 6px 24px;
      border-radius: 4px;
    }
  }


  .box-card{
    min-height: 200px;
    color: #E5EAF1;
    font-size: 14px;
    font-weight: 400;
    background: linear-gradient(#7584AA,#8E9CBD);
    border: 0px solid #EBEEF5;
  }

  .el-divider--horizontal {
    margin: 6px 0;
    height: 2px;
    background: #6083BC52;
  }

  .itemClass {
    background: linear-gradient(#7584AA,#8E9CBD);

    .title{
      color: #E5EAF1;
      font-size: 14px;
      font-weight: 400;
      height: 48px;
      display:flex;
      align-items: center;
      padding-left: 10px;
    }

    .other{
      height: 0px;
      color: #D9D9D9;
      font-size: 12px;
      font-weight: 600;
      display: none;

      .actor{
        padding: 10px;
      }

      .num{
        margin-left: 30px;
        padding: 10px;
      }

      .type{
        margin-left: 60px;
        padding: 10px;
        background: radial-gradient(ellipse 20px 8px at 50%, #c5e0b4b7, #fff0);
      }
    }

    &:hover {
      cursor: pointer;
      background: linear-gradient(#2B458F,#8E9CBD);

      .title{
        color: #E5EAF1;
        font-weight: 800;
      }

      .other{
        height: 100%;
        display: flex;
      }
    }
  }

  .wordcloud {
    width: 100%;
    height: 260px;
  }
  .maprow{

    display:flex;
    align-items:center;     //垂直居中
    justify-content:center; //水平居中


    .map {
      width: 70%;
      height: 360px;
    }

  }


  .chartCategory{
    width: 100%;
    height: 200px;
  }
  .chartPie{
    width: 100%;
    height: 200px;
  }
}

</style>
