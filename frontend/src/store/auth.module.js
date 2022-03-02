import axios from 'axios'
import Vue from 'vue'

const URL_AUTH = 'http://localhost:8000/api/v1/auth/token'
const URL_USERS = 'http://localhost:8000/api/v1/users/'

const HTTP_BAD_REQUEST = 400
const HTTP_UNAUTHORIZED = 401

export default {
  state: {
    username: null,
    token: null,
    isAuthenticated: false
  },
  getters: {
    getUsername(state) {
      return state.username
    },
    getToken(state) {
      return state.token
    },
    getAuthHeader(state) {
      return {headers: {'Authorization': 'Bearer ' + state.token}}
    },
    isAuthenticated(state) {
      return state.isAuthenticated
    }
  },
  actions: {
    async login(context, credentials) {
      var data = 'grant_type=password&username=' + credentials.username + '&password=' + credentials.password

      try {
        var response = await axios.post(URL_AUTH, data)
      } catch (error) {
        if (error.response.status == HTTP_UNAUTHORIZED) {
          Vue.swal('Invalid credentials!', 'Check the credentials are valid.', 'error')
        }
        return
      }

      var token = response.data.access_token

      context.commit('setToken', token)
      context.commit('setUsername', credentials.username)
    },
    async register(context, credentials) {
      try {
        await axios.post(URL_USERS, credentials)
      } catch (error) {
        if (error.response.status == HTTP_BAD_REQUEST) {
          await Vue.swal('Bad request!', error.response.data.detail + '.', 'error')
        }
        return
      }
    },
    logOut(context) {
      context.commit('setToken', null)
      context.commit('setUsername', null)
    }
  },
  mutations: {
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = state.token ? true : false
    },
    setUsername(state, username) {
      state.username = username
    },
  }
}
