import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import LogOut from '../views/LogOut.vue'
import Profile from '../views/Profile.vue'
import NewGame from '../views/NewGame.vue'
import JoinRoom from '../views/JoinRoom.vue'
import Room from '../views/Room.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/register/',
    name: 'Register',
    component: Register
  },
  {
    path: '/login/',
    name: 'Login',
    component: Login
  },
  {
    path: '/log-out/',
    name: 'LogOut',
    component: LogOut
  },
  {
    path: '/profile/',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/new-game/',
    name: 'NewGame',
    component: NewGame
  },
  {
    path: '/room/:roomCode',
    name: 'Room',
    component: Room
  },
  {
    path: '/join-room/:roomCode',
    name: 'JoinRoom',
    component: JoinRoom
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
