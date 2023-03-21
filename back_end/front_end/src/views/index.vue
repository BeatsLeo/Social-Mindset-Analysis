<template>
  <div class="indexView">
    <el-container>
      <el-header>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
          background-color="#526B9C"
          text-color="#fff"
          active-text-color="#ffd04b">
          <el-menu-item index="1">首页</el-menu-item>
          <el-menu-item index="2">热点事件</el-menu-item>
          <el-menu-item index="3">心态分析</el-menu-item>
          <el-menu-item index="4">心态调整建议库</el-menu-item>
        </el-menu>
        <div class="right">
          <el-button type="text" @click="userInfo()"><i class="el-icon-user-solid"></i></el-button>
          <el-button type="text" @click="systemSetting()"><i class="el-icon-s-tools"></i></el-button>
        </div>
      </el-header>
      <el-main class="main">
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>

export default {
  components: {
  },
  data() {
    return {
      activeIndex: "",
    };
  },
  mounted() {
    if(this.$route.query.active === undefined){
      this.activeIndex = "1";
    }else{
      this.activeIndex = this.$route.query.active;
    }
  },
  methods: {
    handleSelect(index){
      let gotopath = "";
      if(index === "1"){
        gotopath = "/main";
      }else if(index === "2"){
        gotopath = "/hotpoint";
      }else if(index === "3"){
        gotopath = "/analysis";
      }else if(index === "4"){
        gotopath = "/suggest";
      }else{
        return;
      }

      this.$router.push({
        path: gotopath,
        query: {
          active: index
        },
      },()=>{},()=>{});
    },
  },
};
</script>

<style lang="less">
.indexView {
  width:100%;
  height:100%;

  .el-header {
    padding: 0;
    display: flex;

    .right{
      position: absolute;
      top: 14px;
      right: 40px;

      .el-button--text{
        font-size: 24px;
      }
    }
  }
  .el-menu {
    padding-left: 40px;
    width: 100%;
    height: 100%;
  }

  .main {
    background: #E5EAF1;
    height: 100%;
    min-height: 700px;
    padding-top: 5px;
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: 20px;
  }
}
</style>
