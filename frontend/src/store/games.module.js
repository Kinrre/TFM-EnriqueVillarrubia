import axios from 'axios'
import Vue from 'vue'

import router from '../router'

const URL_GAMES = 'http://localhost:8000/api/v1/games/?skip=0&limit=100'
const URL_ME_GAMES = 'http://localhost:8000/api/v1/users/me/games/?skip=0&limit=100'
const URL_USERS = 'http://localhost:8000/api/v1/users/id/'
const URL_CREATE_GAME = 'http://localhost:8000/api/v1/users/me/games/'
const URL_TRAIN_GAME = 'http://localhost:8002/api/v1/train/'
const URL_CHECK_MOVEMENT = 'http://localhost:8002/api/v1/movements/'

const HTTP_BAD_REQUEST = 400
const HTTP_UNAUTHORIZED = 401

export default {
  state: {
    games: null,
    trainingSuccessful: false,
    validMovement: false
  },
  getters: {
    getGames(state) {
      return state.games
    },
    isTrainingSuccessful(state) {
      return state.trainingSuccessful
    },
    isValidMovement(state) {
      return state.validMovement
    }
  },
  actions: {
    async getGames(context) {
      var response = await axios.get(URL_GAMES)
      var games = response.data
      var cache = {}
      
      for (let i = 0; i < games.length; i++) {
        let game = games[i]
        let owner_id = game.owner_id

        if (!cache[owner_id]) {
          let response_owner = await axios.get(URL_USERS + owner_id)
          cache[owner_id] = response_owner.data.username
        }

        games[i].username = cache[owner_id]
      }

      context.commit('setGames', games)
    },
    async getMeGames(context) {
      var authHeader = context.getters.getAuthHeader

      try {
        var response = await axios.get(URL_ME_GAMES, authHeader)
      } catch (error) {
        if (error.response.status == HTTP_UNAUTHORIZED) {
          // Remove token
          context.commit('setToken', null)

          // Go to login
          router.push('/login/')
        }
        return
      }

      var games = response.data
      
      for (let i = 0; i < games.length; i++) {
        games[i].username = context.getters.getUsername
      }

      context.commit('setGames', games)
    },
    async createGame(context, payload) {
      var authHeader = context.getters.getAuthHeader

      try {
        await axios.post(URL_CREATE_GAME, payload, authHeader)
        await Vue.swal('Success!', 'The game has been successfully created.', 'success')

        // Go to the profile
        router.push('/profile/')
      } catch (error) {
        if (error.response.status == HTTP_BAD_REQUEST) {
          Vue.swal('Bad request!', error.response.data.detail + '.', 'error')
        } else if (error.response.status == HTTP_UNAUTHORIZED) {
          // Remove token
          context.commit('setToken', null)

          // Go to login
          router.push('/login/')
        }
        return
      }      
    },
    async trainGame(context, id) {
      Vue.swal.showLoading()

      try {
        await axios.post(URL_TRAIN_GAME + id)
      } catch (error) {
        if (error.response.status == HTTP_BAD_REQUEST) {
          context.commit('setTrainingSuccuessful', false)
          Vue.swal('Bad request!', error.response.data.detail + '.', 'error')
        }
        return
      }

      Vue.swal('Successful!', 'Your game is beeing trained in the system.', 'success')

      context.commit('setTrainingSuccuessful', true)
    },
    async checkMovement(context, payload) {
      try {
        var response = await axios.post(URL_CHECK_MOVEMENT, payload)
      } catch (error) {
        if (error.response.status == HTTP_BAD_REQUEST) {
          context.commit('setValidMovement', false)
          Vue.swal('Bad request!', error.response.data.detail + '.', 'error')
        }
        return
      }
      
      context.commit('setValidMovement', response.data.valid)
    }
  },
  mutations: {
    setGames(state, games) {
      state.games = games
    },
    setTrainingSuccuessful(state, value) {
      state.trainingSuccessful = value
    },
    setValidMovement(state, value) {
      state.validMovement = value
    }
  }
}
