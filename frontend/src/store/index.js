import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

import auth from './auth.module.js'
import games from './games.module.js'
import room from './room.module.js'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    auth,
    games,
    room
  },
  plugins: [createPersistedState()]
})
