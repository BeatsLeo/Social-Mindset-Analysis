<template>
  <div class="suggestView">
    <el-col :span="11">
      <h2><i class="el-icon-s-opportunity"></i>&nbsp;心态列表</h2>
      <el-divider></el-divider>
      <el-row class="mentality">
        <el-radio-group v-model="mentality" size="small" @input="suggest()">
          <div v-for="(item, index) in mentalityData" :key="item.group">
            <el-row :class="['row'+(index+1)]">
              <span class="title">{{item.group}}</span>
              <div  v-for="(i,j) in item.options" :key="i.id">
                <el-radio-button :label="i.id" :class="['i'+(j+1)]">{{i.name}}</el-radio-button>
              </div>
            </el-row>
          </div>
        </el-radio-group>
      </el-row>
      <br>
      <el-row>
        <h2><i class="el-icon-s-opportunity"></i>&nbsp;【x心态】的针对性调整建议</h2>
        <el-divider></el-divider>
        <el-card class="box-card">
          <span>
            {{suggestContent}}
          </span>
        </el-card>
      </el-row>
    </el-col>

    <el-col :span="2">&nbsp;</el-col>

    <el-col :span="11">
      <el-row>
        <h2><i class="el-icon-s-opportunity"></i>&nbsp;心态列表</h2>
        <el-divider></el-divider>
      </el-row>
      <el-row>
        <div class="h3div">
          <h3>事件</h3>
        </div>
        <el-input placeholder="关键词检索..." v-model="e" class="input-with-select" size="mini"/>
      </el-row>
      <el-row>
        <div class="h3div">
          <h3>心态</h3>
        </div>
        <el-input placeholder="关键词检索..." v-model="m" class="input-with-select" size="mini"/>
      </el-row>
      <el-row>
        <el-button class="handleButton" @click="handle()" type="primary" round>点击生成</el-button>  
      </el-row>
      <el-row>
        <div class="h3div">
          <h3>建议生成结果</h3>
        </div>
        <el-card class="box-card">
          <span>
            {{handleContent}}
          </span>
        </el-card>
      </el-row>
    </el-col>
  </div>
</template>

<script>
import ajax from '../axios';
import mentalityData from "../testdata/mentalityData";

export default {
  data () {
    return {
      mentality: "",
      e: "",
      m: "",

      mentalityData,

      suggestContent:"",
      handleContent:""

    }
  },
  components: {
  },
  mounted() {
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
    handle(){
      this.handleContent= this.e + "===="+this.m+ "======为贯彻落实我党“加快用互联网信息技术推进社会治理”的要求，本项目拟构建基于开放域事件提取的社会心态交互式挖掘与引导系统，挖掘社会心态的演化机制，摸清其事件原因。依托Erlangshen-Bert等预训练模型，本项目提出基于人在环路、开放域事件抽取与分析的技术框架，形成针对社会心态的智能监控、分析、归因和引导的一体化解决方案，为社会治理提供建议";
    
      ajax({
        url: '/xx/handle.json',
        method: 'get',
        params: {
          e: this.e,
          m: this.m
        }
      })
        .then((data) => {
          if(data.flag === false){
            this.$message.info('获取信息失败');
            return;
          }
          this.handleContent = data.data;
        })
        .catch((error) => {
          this.$message.error('接口调用异常：'+error);
        })
        .finally(() => {
        });
      }
  }
}
</script>

<style lang="less">
.suggestView{
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

  .mentality{
    
    .el-row{
      display: flex;
      justify-content: flex-start;
      align-items: center;

      margin-left: 20px;
      margin-top: 10px;
      margin-bottom: 10px;

      padding: 6px 6px 6px 6px;
      border-radius: 4px;
    }

    .el-radio-button{
      margin-right: 2px;
      
    }
    .el-radio-button__inner{
      border-radius: 0 0 0 0;
      border: 0;
      min-width: 100px;
      font-size: 14px;
    }

    .title{
      font-size: 14px;
      font-weight: 500;
      padding-left: 20px;
      padding-right: 40px;
    }
    .i1{
      filter: grayscale(80%)
    }
    .i2{
      filter: grayscale(60%)
    }
    .i3{
      filter: grayscale(40%)
    }
    .i4{
      filter: grayscale(20%)
    }
    .i5{
      filter: grayscale(0%)
    }

    .row1{
      color: #E6AD00;
      background: #fff2cc30;
      .el-radio-button__inner{
        background: #fac94475;
      }
    }
    .row2{
      color: #2B458F;
      background: #839fcc30;
      .el-radio-button__inner{
        background: #1540b835;
      }
    }
    .row3{
      color: #548235;
      background: #c5e0b430;
      .el-radio-button__inner{
        background: #a9d18e75;
      }
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
  .handleButton{
    margin-top: 20px;
  }
}

</style>
