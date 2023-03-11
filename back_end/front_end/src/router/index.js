import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: 'login',
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/register.vue'),
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
          path: '/analysisdetail',
          name: 'analysisdetail',
          component: () => import('@/views/analysisdetail.vue'),
        },
        {
          path: '/analysis',
          name: 'analysis',
          component: () => import('@/views/analysis.vue'),
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
