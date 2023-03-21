<template>
  <div class="loginView">
    <div class="login">
        <h1>开放域社会心态挖掘与引导系统</h1>
        <el-divider></el-divider>
        <el-input class="input" prefix-icon="el-icon-user" v-model="username" placeholder="账号"></el-input>
        <el-input class="input" prefix-icon="el-icon-lock" v-model="password" placeholder="密码" show-password></el-input>
        <el-row>
          <el-col :span="12">
          <el-input prefix-icon="el-icon-key" v-model="code" placeholder="验证码"></el-input>
          </el-col>
        <el-col :span="2">&nbsp;</el-col>
          <el-col :span="10">
            <div @click="refreshCode()">
              <identify :identifyCode="identifyCode"></identify>
            </div>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
        <el-button class="loginButton" @click="login()" type="primary" round>点此登陆</el-button>
          </el-col>
          <el-col :span="2">&nbsp;</el-col>
          <el-col :span="10">
        <el-button class="loginButton" @click="register()" type="primary" round>点此注册</el-button>
          </el-col>
        </el-row>
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
      code: "",
      identifyCode: "",
      identifyCodes: "0123456789abcdwerwshdjeJKDHRJHKOOPLMKQ",//随便打的
    }
  },
  components: {
    Identify
  },
  mounted() {
    this.refreshCode();
  },
  methods: {
    getCookie (name) {
      var value = '; ' + document.cookie
      var parts = value.split('; ' + name + '=')
      if (parts.length === 2) return parts.pop().split(';').shift()
    },
    refreshCode() {
      this.identifyCode = "";
      this.makeCode(this.identifyCodes,4);
    },
    register() {
      this.$router.push({
            path: '/register',
            query: {
            },
          });
    },
    randomNum (min, max) {
      max = max + 1
      return Math.floor(Math.random() * (max - min) + min)
    },
    // 随机生成验证码字符串
    makeCode (data, len) {
      for (let i = 0; i < len; i++) {
        this.identifyCode += data[this.randomNum(0, data.length - 1)]
      }
    },
    login() {
      if(this.identifyCode.toLowerCase() !== this.code.toLowerCase()){
        this.$message.error('请输入正确的验证码');
        return;
      }
      let md5Password = md5(this.password);
      this.$message.info('调用登陆: '+this.username+ '  '+ this.password + '  ' + md5Password);
      ajax({
        url: 'http://127.0.0.1:8000/api/login/',
        method: 'post',
        data: {
          l_username: this.username,
          l_password: this.password,
        },
      })
        .then((data) => {
          if(data.flag === false){
            this.$message.info('登陆失败');
            return;
          }
          this.$message.info('登陆成功');
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
            path: '/main',
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
.loginView {
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
.login {
  width:25%;
  margin-right: 15%;
}
.input{
  margin-bottom: 20px;
}
.loginButton{
  width: 100%;
  margin-top: 20px;
}

h1, h2 {
  color: #fff;
}
</style>
