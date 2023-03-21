<template>
    <div class="hotpointView">
      <el-col :span="11">
        <h2><i class="el-icon-s-opportunity"></i>&nbsp;心态背后事件导向</h2>
        <el-divider></el-divider>
        <el-row class="listquery">
          <el-col :span="10">
            <el-select v-model="query_dq" multiple collapse-tags placeholder="地区" @change="search()" size="mini">
              <el-option
                v-for="item in dqData"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="14">
            <el-date-picker
              v-model="query_date"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              size="mini"
              @blur="search()">
            </el-date-picker>
          </el-col>
        </el-row>
        <el-row>
        <el-card class="box-card">
          <span>
            <el-row v-for="(item) in hotList" :key="item.id">
        <div class="itemClass" @click="detail(item)">
          <div class="title">
            <span>{{item.name}}</span>
          </div>
          <div class="other">
            <span class="num"><i class="el-icon-s-opportunity"></i>{{item.num}}</span>
            <span class="type">{{item.type}}</span>
          </div>
        </div>
      </el-row>
          </span>
        </el-card>
      </el-row>
      </el-col>

      <el-col :span="2">&nbsp;</el-col>

      <el-col :span="11">
        <el-row>
        <h2><i class="el-icon-s-opportunity"></i>&nbsp;引导建议</h2>
        <el-divider></el-divider>
        <el-card class="box-card2">
          <span>
            1.允许自己感受悲伤：悲伤是一种自然的情绪，我们不应该试图压抑或避免它。相反，我们应该允许自己感受悲伤，并找到一种健康的方式来处理它。<br><br>

2.寻找支持：与朋友或家人分享你的感受，或者寻求专业人士的帮助，例如心理医生或社会工作者。他们可以提供有用的建议和支持，让你更好地处理自己的情绪。<br><br>

3.接受变化：悲伤情绪可能与某些变化和挑战有关，例如失去亲人、失业等等。要学会接受这些变化，并尝试从中寻找积极的方面。<br>
          </span>
        </el-card>
      </el-row>
      <el-row v-if="ShowPage">
        <h2><i class="el-icon-cloudy"></i>&nbsp;评论词云</h2>
        <el-divider></el-divider>
        <div class="wordcloud">
          <word-cloud :worddata="wordData"></word-cloud>
        </div>
      </el-row>
      </el-col>
    </div>
  </template>

  <script>
  import ajax from '../axios';
  import wordCloud from '@/components/wordCloud.vue';
  import qs from "qs";

  export default {
    data () {
      return {
        searchLoading: false,

        hotList:[],
        wordData:[],
        dqData:[],
        suggestContent:"",
        query_dq: "",
        query_date: "",
        ShowPage:false,
        flag_word_cloud:false,

        pageSize: 7
      }
    },
    components: {
      wordCloud,
    },
    mounted() {
      this.search();
    },
    methods: {
    suggest(){
      this.suggestContent = this.mentality+"====所谓引导建议，关键是引导建议需要如何写。 引导建议的发生，到底需要如何做到，不引导建议的发生，又会如何产生。 就我个人来说，引导建议对我的意义，不能不说非常重大。 而这些并不是完全重要，更加重要的问题是， 既然如此， 一般来讲，我们都必须务必慎重的考虑考虑。 伏尔泰在不经意间这样说过，不经巨大的困难，不会有伟大的事业。我希望诸位也能好好地体会这句话。 引导建议，发生了会如何，不发生又会如何。【放一点废话】";
      ajax({
        url: '/xx/suggest.json',
        method: 'get',
        params: {
          mentality: this.mentality
        }
      })
        .then((data) => {
          if(data.flag === false){
            this.$message.info('获取信息失败');
            return;
          }
          this.suggestContent = data.data;
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
    },
      search(){
        this.id=this.$route.query.id;
        this.searchLoading = true;
        if(this.query_date){
        for(var i=0;i<=1;i++){
          this.query_date[i] = this.dayjs(this.query_date[i]).format("YYYY-MM-DD")
        }
      }
      var da={}
      da={
          id:this.id,
          dq:this.query_dq ,
          date: this.query_date,
          curPage: 0,
          pageSize: this.pageSize,
      }
      da=qs.stringify(da,{arrayFormat:'repeat'})
        ajax({
          url: 'http://127.0.0.1:8000/api/xtfx/comments_detail/?'+da,
          method: 'get'
        })
          .then((data) => {
           if (data['respCode'] === '000000') {
            this.hotList = data['event_list']
            this.dqData = data['province_map']
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
        ajax({
        url: 'http://127.0.0.1:8000/api/xtfx/comment_cloud/',
        method: 'get',
        params: {
          id:this.id,
        }
      })
        .then((data) => {
          console.log("event_cloud:",JSON.parse(JSON.stringify(data)))
          this.wordData=JSON.parse(JSON.stringify(data));
          this.ShowPage = true;
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
      },
      nextPage(){
        // 多加载pageSize条记录
        this.pageSize = this.pageSize * 2;
        this.search();
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
      }
    }
  }
  </script>

  <style lang="less">
  .hotpointView{
    width:100%;
    height:100%;

    .listquery{
      margin-bottom: 10px;
      .el-input-group{
        width: 95%;
      }
    }

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
          padding: 10px;
        }

        .type{
          margin-left: 400px;
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
    .map {
      width: 100%;
      height: 260px;
    }
    .chartCategory{
      width: 100%;
      height: 260px;
    }
    .box-card{
    min-height: 500px;
    color: #E5EAF1;
    font-size: 14px;
    font-weight: 400;
    background: linear-gradient(#7584AA,#8E9CBD);
    border: 0px solid #EBEEF5;
  }
    .box-card2{
    min-height: 200px;
    color: #E5EAF1;
    font-size: 14px;
    font-weight: 400;
    background: linear-gradient(#7584AA,#8E9CBD);
    border: 0px solid #EBEEF5;
  }
  }

  </style>
