<template>
    <div class="registerView">
      <div class="register">
          <h1>注&nbsp;&nbsp;&nbsp;&nbsp;册</h1>
          <el-divider></el-divider>
          <el-input class="input" prefix-icon="el-icon-user" v-model="username" placeholder="账号"></el-input>
          <el-input class="input" prefix-icon="el-icon-lock" v-model="password" placeholder="密码" show-password></el-input>
          <el-input class="input" prefix-icon="el-icon-lock" v-model="passcheck" placeholder="确认密码" show-password></el-input>
          <el-divider></el-divider>
          <h3>密码应包含，至少【】位</h3>
          <el-button class="registerButton" @click="register()" type="primary" round>点此注册</el-button>
      </div>
    </div>
  </template>

  <script>
  import ajax from '../axios';
  import Identify from '@/components/identify.vue';
  import md5 from 'js-md5';

  export default {
    data () {
      return {
        username: "",
        password: "",
        passcheck: "",
        code: "",
        identifyCode: "",
        identifyCodes: "0123456789abcdwerwshdjeJKDHRJHKOOPLMKQ",//随便打的
      }
    },
    components: {
      Identify
    },
    mounted() {
    },
    methods: {
      register() {
        let md5Password = md5(this.password);
        ajax({
          url: '/api/regist/',
          method: 'post',
          data: {
            username: this.username,
            password: this.password,
          }
        })
          .then((data) => {
            if(data.flag === false){
              this.$message.info('注册失败');
              return;
            }
            this.$message.info('注册成功');
            //跳主页
            this.$router.push({
              path: '/main',
              query: {
              },
            });
          })
          .catch((error) => {
            this.$message.error('接口调用异常：'+error);

            //这里测试使用，正式用的时候要删除
            this.$router.push({
              path: '/login',
              query: {
              },
            });

          })
          .finally(() => {
          });
      }
    },
  }
  </script>

  <style scoped>
  .registerView {
    background:url("../assets/login.gif");
    width:100%;
    height:100%;
    position:fixed;
    display:flex;
    justify-content: flex-end;
    align-items: center;
    background-size:100% 100%;
    margin:0;
    padding:0;
    border:0;
  }
  .register {
    width:25%;
    margin-right: 15%;
  }
  .input{
    margin-bottom: 20px;
  }
  .registerButton{
    width: 100%;
    margin-top: 20px;
  }

  h1, h2 {
    color: #fff;
  }
  </style>
