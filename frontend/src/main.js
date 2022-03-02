import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'

import './plugins/bootstrap-vue'

import VueSocketIO from 'vue-socket.io'

import VueSweetalert2 from 'vue-sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'

import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false

Vue.use(new VueSocketIO({
  debug: false,
  connection: 'http://localhost:8001/',
  options: {autoConnect: false}
}))

Vue.use(VueSweetalert2)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
