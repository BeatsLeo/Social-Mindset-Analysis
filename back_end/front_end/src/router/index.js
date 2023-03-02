import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: 'index',
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login.vue'),
    },
    {
      path: '/index',
      name: 'index',
      component: () => import('@/views/index.vue'),
      redirect: '/main',
      children: [
        {
          path: '/main',
          name: 'main',
          component: () => import('@/views/main.vue'),
        },
        {
          path: '/hotpoint',
          name: 'hotpoint',
          component: () => import('@/views/hotpoint.vue'),
        },
        {
          path: '/hotpointdetail',
          name: 'hotpointdetail',
          component: () => import('@/views/hotpointdetail.vue'),
        },
        {
          path: '/analyse',
          name: 'analyse',
          component: () => import('@/views/analyse.vue'),
        },
        {
          path: '/suggest',
          name: 'suggest',
          component: () => import('@/views/suggest.vue'),
        },
      ]
    },
    // {
    //   path: '/main',
    //   name: 'main',
    //   component: () => import('@/views/main.vue'),
    // }
  ]
})
