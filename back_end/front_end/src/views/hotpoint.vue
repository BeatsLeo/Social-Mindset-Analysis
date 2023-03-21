<template>
  <div class="hotpointView">
    <el-col :span="11">
      <h2><i class="el-icon-s-opportunity"></i>&nbsp;热点事件列表</h2>
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
      <el-row class="listquery">
        <el-col :span="10">
          <el-select v-model="query_mentality" multiple collapse-tags placeholder="心态" @change="search()" size="mini">
            <el-option-group
              v-for="item in mentalityData"
              :key="item.group"
              :label="item.group">
              <el-option
                v-for="i in item.options"
                :key="i.id"
                :label="i.name"
                :value="i.id">
              </el-option>
            </el-option-group>
          </el-select>
        </el-col>
        <el-col :span="14">
          <el-input placeholder="关键词检索..." v-model="query_key" class="input-with-select" size="mini">
            <el-button slot="append" icon="el-icon-search" @click="search()" :loading="searchLoading" size="mini"></el-button>
          </el-input>
        </el-col>
      </el-row>
<!--      .slice((currpage-1)*eachpage,currpage*eachpage)-->
      <el-row v-for="(item) in hotList" :key="item.id">
        <div class="itemClass" @click="detail(item)">
          <div class="title">
            <span>{{item.name}}</span>
          </div>
          <div class="other">
            <span class="actor">{{item.actor}}</span>
            <span class="num"><i class="iconfont icon-huoyan"></i>{{item.num}}</span>
            <span class="type">{{item.type}}</span>
          </div>
        </div>
      </el-row>
      <el-row>
        <!--<el-button type="text" icon="el-icon-arrow-down" @click="nextPage()">展开列表</el-button>-->
        <div style="float:right;margin-right:50px;">
        <span v-if="currpage>1" @click="changePage(currpage,page_flag=false)">上一页</span>
        <span>{{currpage}}</span>/<span>{{pagesum}}</span>
        <span v-if="currpage<pagesum" @click="changePage(currpage,page_flag=true)">下一页</span>
        </div>
      </el-row>
    </el-col>

    <el-col :span="2">&nbsp;</el-col>

    <el-col :span="11" v-if="ShowPage">
      <el-row>
        <h2><i class="el-icon-cloudy"></i>&nbsp;热点事件关键词云</h2>
        <el-divider></el-divider>
        <div class="wordcloud">
          <word-cloud :worddata="wordData"></word-cloud>
        </div>
      </el-row>
      <el-row>
        <h2><i class="el-icon-s-opportunity"></i>&nbsp;热点地区热力图</h2>
        <el-divider></el-divider>
        <el-col :span="12">
          <div class="map">
            <china-map :attitude_color="mapData"></china-map>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="chartCategory">
            <chart-category :hot_count="chartCategoryData"></chart-category>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </div>
</template>

<script>
import ajax from '../axios';
import qs from 'qs';
import wordCloud from '@/components/wordCloud.vue';
import ChinaMap from '@/components/chinaMap.vue';
import ChartCategory from '@/components/chartCategory_hot.vue';
import mentalityData from "../testdata/mentalityData";
import "../assets/icon/font/iconfont.css"

export default {
  data () {
    return {
      searchLoading: false,

      hotList:[],
      wordData:[],
      mapData:[],
      chartCategoryData:[],
      dqData:[],
      mentalityData,
      ShowPage:false,
      flag_map:false,
      flag_column:false,
      flag_word_cloud:false,
      page_flag:false,

      query_dq: "",
      query_mentality: "",
      query_date: "",
      query_key: "",

      pageSize: 7,
      pagesum: "", //总页数
      currpage: 1, //当前页数
      eachpage: 8, //每页行数
    }
  },
  components: {
    wordCloud,
    ChinaMap,
    ChartCategory,
  },
  mounted() {
    this.search();
    // this.changePage();
  },
  methods: {
    getStaffList:function(){
            var _this = this;
            alert("1")
            this.$http.post(
                _this.baseUrl+"/StaffController/getStaffList",
                {}
            ).then(function(result){
                var res = result.body;
                if(res.resultCode="0000"){
                    alert
                    _this.staffList=res.data;
                    _this.pagesum = Math.ceil(_this.staffList.length/_this.eachpage);
                }else{
                    alert(res.resultMsg);
                }
            });
          },
    changePage(){
      var da={}
      da={
          dq:this.query_dq ,
          mentality: this.query_mentality,
          date: this.query_date,
          key: this.query_key,
          flag:this.page_flag,
          curpage:this.currpage,
      }
      da=qs.stringify(da,{arrayFormat:'repeat'})
      ajax({
        url: '/api/rdsj/event_list/?'+da,
        method: 'get',
      })
        .then((data) => {
          if (data['respCode'] === '000000') {
            this.hotList = data['event_list']
            this.pagesum= data['count_page']
            this.dqData = data['province_map']
            if(this.page_flag){
              this.currpage++
            }
            else {
              this.currpage--
            }
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
    search(){
      this.searchLoading = true;
      if(this.query_date){
        for(var i=0;i<=1;i++){
          this.query_date[i] = this.dayjs(this.query_date[i]).format("YYYY-MM-DD")
        }
      }
      var da={}
      da={
          dq:this.query_dq ,
          mentality: this.query_mentality,
          date: this.query_date,
          key: this.query_key,
      }
      da=qs.stringify(da,{arrayFormat:'repeat'})
      ajax({
        url: '/api/rdsj/event_list/?'+da,
        method: 'get',
      })
        .then((data) => {
          if (data['respCode'] === '000000') {
            this.hotList = data['event_list']
            console.log(this.hotList)
            this.pagesum= data['count_page']
            console.log(this.pagesum)
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
        url: '/api/index/attitude_map/',
        method: 'get',
        params: {
        }
      })

        .then((data) => {
          console.log("attitude_map:",JSON.parse(JSON.stringify(data)))
          this.mapData=JSON.parse(JSON.stringify(data));
          this.flag_map=true;
          if(this.flag_column&&this.flag_word_cloud){
            this.ShowPage = true;
          }
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
          this.flag_column=true;
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
        url: '/api/index/event_cloud/',
        method: 'get',
        params: {
        }
      })
        .then((data) => {
          console.log("event_cloud:",JSON.parse(JSON.stringify(data)))
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
        //float: right;
        margin-left: 440px;
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
}

</style>
