import { createRouter, createWebHistory } from 'vue-router'
import { session } from './data/session'
import { userResource } from '@/data/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
  },
  {
    name: 'Login',
    path: '/account/login',
    component: () => import('@/pages/Login.vue'),
  },
  {
    name: 'Books',
    path: '/books/books',
    component: () => import('@/pages/Books.vue'),
  },
  {
    name: 'Member',
    path: '/member/member',
    component: () => import('@/pages/Member.vue'),
  },
  {
    name: 'AddMember',
    path: '/addmember',
    component: () => import('@/pages/AddMember.vue'),
  },
  
  {
    name: 'Transactions',
    path: '/transactions', // Lowercase path
    component: () => import('@/pages/Transactions.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn

  try {
    if (userResource.promise) {
      await userResource.promise
    }
  } catch (error) {
    isLoggedIn = false
  }

  if (to.name === 'Login' && isLoggedIn) {
    next({ name: 'Home' })
  } else if (to.name !== 'Login' && !isLoggedIn) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
