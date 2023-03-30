<template>
  <div class="mainView">
    <el-row class="header">
      <el-col :span="2">&nbsp;</el-col>
      <el-col :span="20">
        <h1>智能心态分析系统</h1>
        <span>为贯彻落实我党“加快用互联网信息技术推进社会治理”的要求，本平台拟构建基于开放域事件提取的社会心态交互式挖掘与引导系统，挖掘社会心态的演化机制，摸清其事件原因。依托Erlangshen-Bert等预训练模型，本项目提出基于人在环路、开放域事件抽取与分析的技术框架，形成针对社会心态的智能监控、分析、归因和引导的一体化解决方案，为社会治理提供建议。</span>
      </el-col>
      <el-col :span="2">&nbsp;</el-col>
    </el-row>
    <el-row class="content">
      <el-col :span="2">&nbsp;</el-col>
      <el-col :span="11">
        <el-row>
          <h2><i class="el-icon-loading"></i>&nbsp;数据新增折线图</h2>
          <el-divider></el-divider>
          <div>
          <el-col :span="24">
            <chart-line :data="chartData"></chart-line>
          </el-col>
          </div>
          </el-row>
          <el-row>
          <h2><i class="el-icon-loading"></i>&nbsp;热点地区变化时间图</h2>
          <el-divider></el-divider>
          <el-col :span="24">
          <div class="chartCategory" v-if="ShowPage_column">
            <chart-category :hot_count="chartCategoryData"></chart-category>
          </div>
        </el-col>
          </el-row>
        <el-row>
        <h2><i class="el-icon-s-opportunity"></i>&nbsp;心态分布图</h2>
        <el-divider></el-divider>
        <div class="map" v-if="ShowPage_map">
          <china-map :attitude_color="mapData"></china-map>
        </div>
      </el-row>

      </el-col>
      <el-col :span="2">&nbsp;</el-col>
      <el-col :span="9">
        <h2><i class="el-icon-s-opportunity"></i>&nbsp;部分热点事件展示</h2>
        <el-divider></el-divider>
        <el-row v-for="(item) in hotList" :key="item.id">
          <div class="itemClass" @click="detail(item)">
            <div class="title">
              <span>{{item.name}}</span>
            </div>
            <div class="other">
              <span class="actor">{{item.actor}}</span>
              <span class="num"><i class="el-icon-s-opportunity"></i>{{item.num}}</span>
              <span class="type">{{item.type}}</span>
            </div>
          </div>
        </el-row>
          <el-row>
          <h2><i class="el-icon-sort"></i>&nbsp;心态变化时间图</h2>
          <el-divider></el-divider>
          <el-col :span="24">
            <div class="chartCategory" v-if="ShowPage_pie">
              <chart-pie :attitude_count="chartPieData"></chart-pie>
            </div>
          </el-col>
          </el-row>
          <el-row>
          <h2><i class="el-icon-cloudy"></i>&nbsp;词云</h2>
          <el-divider></el-divider>
          <div class="wordcloud" v-if="ShowPage_word">
          <word-cloud :worddata="wordData"></word-cloud>
          </div>
          </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import ajax from '../axios';
import ChinaMap from '@/components/chinaMap.vue';
import "../assets/icon/font/iconfont.css"
import wordCloud from '@/components/wordCloud.vue';
import ChartCategory from '@/components/chartCategory_hot.vue';
import ChartPie from '@/components/chartPie.vue';
import ChartLine from '@/components/chartLine.vue';


export default {
  data () {
    return {
      searchKeys: "",
      searchLoading: false,
      activeName: 1,
      ShowPage:false,
      hotList:[],
      mapData:[],
      wordData:[],
      chartCategoryData:[],
      chartPieData:[],
      ShowPage_word:false,
      ShowPage_map:false,
      ShowPage_pie:false,
      ShowPage_column:false,
      chartData: [
        { time: '2021-01-01', value: 10 },
        { time: '2021-01-02', value: 20 },
        { time: '2021-01-03', value: 30 },
        { time: '2021-01-04', value: 40 },
        { time: '2021-01-05', value: 50 }
      ]
    }
  },
  components: {
    ChinaMap,
    wordCloud,
    ChartCategory,
    ChartPie,
    ChartLine,
  },
  mounted() {
    this.init()
  },
  methods: {
    init(){
      ajax({
        url: '/api/index/event_list/',
        method: 'get',
        params: {
        }
      })
        .then((data) => {
          if (data['respCode'] === '000000') {
            console.log('event_list:',data['event_list'])
            this.hotList = data['event_list']
          } else {
            this.$message.error('获取信息失败')
          }
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
      ajax({
        url: '/api/index/attitude_map/',
        method: 'get',
        params: {
        }
      })
        .then((data) => {
          console.log("attitude_map:",JSON.parse(JSON.stringify(data)))
          this.mapData=JSON.parse(JSON.stringify(data));
          this.ShowPage_map = true;
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
      ajax({
        url: '/api/index/attitude_pie/',
        method: 'get',
        params: {
        }
      })
        .then((data) => {
          console.log("attitude_pie:",JSON.parse(JSON.stringify(data)))
          this.chartPieData=JSON.parse(JSON.stringify(data));
          this.ShowPage_pie = true;
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
      ajax({
        url: '/api/index/event_cloud/',
        method: 'get',
        params: {
        }
      })
        .then((data) => {
          console.log("event_cloud:",JSON.parse(JSON.stringify(data)))
          this.wordData=JSON.parse(JSON.stringify(data));
          this.ShowPage_word = true;
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
      ajax({
        url: '/api/index/attitude_column/',
        method: 'get',
        params: {
        }
      })
        .then((data) => {
          console.log("attitude_column:",JSON.parse(JSON.stringify(data)))
          this.chartCategoryData=JSON.parse(JSON.stringify(data));
          this.ShowPage_column = true;
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
    },

    search(){
      if(this.searchKeys === ""){
        this.$message.error('请输入查询内容');
        return;
      }
      this.searchLoading = true;
      ajax({
        url: '/api/index/event_list/',
        method: 'get',
        params: {
          searchKeys: this.searchKeys
        }
      })
        .then((data) => {
          if (data['respCode'] === '000000') {
            this.hotList = data['event_list']
          } else {
            this.$message.error('获取信息失败')
          }
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
          this.searchLoading = false;
        });
    },
    detail(item){
      console.info(item);
      this.$router.push({
        path: "/hotpointdetail",
        query: {
          id: item.id,
          content:item.content,
          active: this.$route.query.active
        },
      },()=>{},()=>{});
    },
    userInfo() {
      this.$message.info('用户信息');
    },
    systemSetting() {
      this.$message.info('系统设置');
    }
  }
}
</script>

<style lang="less">
.mainView{
  width:100%;
  height:100%;

  .header{

    h1 {
      color: #6083BC;
      font-size: 40px;
      margin-block-start: 0px;
      margin-block-end: 10px;
    }

    span{
      color: #37537E;
      font-size: 12px;
    }
  }

  .content{

    h2 {
      font-size: 16px;
      display: flex;
      justify-content: flex-start;
      align-items: center;
      margin-block-start: 10px;
      margin-block-end: 10px;
      margin-left: 10px;
    }

    .el-divider--horizontal {
      margin: 6px 0;
      height: 2px;
      background: #6083BC52;
    }

    .map {
      width: 600px;
      height: 420px;
    }
  }
  .input-with-select{
    margin-top: 10px;
    width: 50%;
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

      .num{
        //margin-left: 30px;
        padding: 10px;
      }

      .type{
        margin-left: 300px;
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
  .chartCategory{
    width: 100%;
    height: 260px;
  }
  .chartLine{
    width: 100%;
    height: 260px;
  }
}




</style>
