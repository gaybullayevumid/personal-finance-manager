import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from './components/LoginPage.vue';
import ProtectedPage from './components/ProtectedPage.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/protected',
    name: 'Protected',
    component: ProtectedPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
