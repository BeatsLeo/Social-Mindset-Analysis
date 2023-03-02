// 引入axios
import axios from 'axios';
import qs from 'qs';
import cookies from "vue-cookies";
import Cookies from 'js-cookie'

export const baseURL = '/';

let getCookie = function (cookie) {
    let reg = /csrftoken=([\w]+)[;]?/g
    return reg.exec(cookie)[1]

}
// 创建实例
const instance = axios.create({
  // `baseURL` 将自动加在 `url` 前面，除非 `url` 是一个绝对 URL。
  // 它可以通过设置一个 `baseURL` 便于为 axios 实例的方法传递相对 URL
  baseURL,
  // `timeout` 指定请求超时的毫秒数。
  // 如果请求时间超过 `timeout` 的值，则请求会被中断
  timeout: 1000 * 10, // 默认值是 `0` (永不超时)
  // 自定义请求头
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  // `withCredentials` 表示跨域请求时是否需要使用凭证
  withCredentials: true,
});

// 添加响应拦截器
instance.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    return response.data;
  },
  config => {
    // config.headers['Content-Type'] = 'application/json;charset=utf-8' // 关键所在
    // config.headers['X-CSRFToken']= this.$cookies.get('csrftoken')
    // config.headers['X-Requested-With'] = 'XMLHttpRequest';
    // config.headers['X-CSRFToken'] = cookie.parse(document.cookie).csrftoken;
    return config
  },
  (error) => {
    // 超出 2xx 范围的状态码都会触发该函数。
    // this.$message.error(error.message); // 统一报错提示
    // 对响应错误做点什么
    return Promise.reject(error);
  }
);

instance.defaults.withCredentials = true;
// request拦截器
instance.interceptors.request.use(
  config => {
    // let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
    // console.log(Cookies.get('name'))
    // console.log(document.cookie.match(regex))
    // config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
    // config.headers['Content-Type'] = 'application/x-www-form-urlencoded' // 关键所在
    // config.headers['X-CSRFToken']= this.$cookies.get('csrftoken')
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    // let cookie = document.cookie;
    // console.log(getCookie(cookie))
    // if(cookie && config.method == 'post'){
    //   config.headers['X-CSRFToken'] = getCookie(cookie);
    // }
    // let cookie = document.cookie;
    // console.log(cookie.parse(document.cookie).csrftoken)
    // config.headers['X-CSRFToken'] = cookie.parse(document.cookie).csrftoken;
    return config
  },
  error => {
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// 导出request
export default function request({
  method = 'get', // 请求方式 默认get
  url = '', // 地址
  data = {}, // post参数
  params = {}, // get参数
}) {
  return instance({
    method,
    url,
    data,
    params,
  });
}

