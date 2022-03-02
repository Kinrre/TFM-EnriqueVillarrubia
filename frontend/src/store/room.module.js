import axios from 'axios'
import Vue from 'vue'

import router from '../router'

const URL_GAME = 'http://localhost:8000/api/v1/matches/?game_id='
const URL_MATCH = 'http://localhost:8000/api/v1/matches/'
const URL_PLAYERS = 'http://localhost:8002/api/v1/players/'

const HTTP_BAD_REQUEST = 400
const HTTP_UNAUTHORIZED = 401
const HTTP_NOT_FOUND = 404

export default {
  state: {
    roomCode: null,
    isRoomCreated: false,

    gameId: null,
    boardSize: null,
    initialBoard: null,

    color: null,
    isActivePlayer: false,
    isCheckingMovement: false
  },
  getters: {
    getRoomCode(state) {
      return state.roomCode
    },
    isRoomCreated(state) {
      return state.isRoomCreated
    },
    getGameId(state) {
      return state.gameId
    },
    getBoardSize(state) {
      return state.boardSize
    },
    getInitialBoard(state) {
      return state.initialBoard
    },
    isActivePlayer(state) {
      return state.isActivePlayer
    },
    isCheckingMovement(state) {
      return state.isCheckingMovement
    },
    getColor(state) {
      return state.color
    }
  },
  actions: {
    async createRoom(context, payload) {
      var url = URL_GAME + payload.gameId

      try {
        var response = await axios.post(url, null, payload.authHeader)
      } catch (error) {
        if (error.response.status == HTTP_UNAUTHORIZED) {
          // Remove token
          context.commit('setToken', null)

          // Go to login
          router.push('/login/')
        } else if (error.response.status == HTTP_NOT_FOUND) {
          Vue.swal('Game not found!', 'Check the game_id is valid.', 'error')
        }
        return
      }

      context.dispatch('commitRoom', response)
      context.commit('setColor', 'white')
    },
    async joinRoom(context, payload) {
      var url = URL_MATCH + '?room_code=' + payload.roomCode

      try {
        var response = await axios.get(url, payload.authHeader)
      } catch (error) {
        if (error.response.status == HTTP_UNAUTHORIZED) {
          // Remove token
          context.commit('setToken', null)

          // Go to login
          router.push('/login/')
        } else if (error.response.status == HTTP_NOT_FOUND) {
          Vue.swal('Room not found!', 'Check the invite link is valid.', 'error')
        }
        return
      }

      context.dispatch('commitRoom', response)
      context.commit('setColor', 'black')
    },
    commitRoom(context, response) {
      var roomInfo = {
        'roomCode': response.data.room_code,
        'gameId': response.data.game.id,
        'boardSize': response.data.game.board_size,
        'initialBoard': response.data.game.initial_board
      }

      context.commit('setRoom', roomInfo)
    },
    async createPlayer(context, payload) {
      try {
        await axios.post(URL_PLAYERS, payload)
      } catch (error) {
        if (error.response.status == HTTP_BAD_REQUEST) {
          Vue.swal('Bad request!', error.response.data.detail + '.', 'error')
        }
      }
    }
  },
  mutations: {
    setRoom(state, roomInfo) {
      state.roomCode = roomInfo.roomCode
      state.isRoomCreated = true

      state.gameId = roomInfo.gameId
      state.boardSize = roomInfo.boardSize
      state.initialBoard = roomInfo.initialBoard
    },
    setColor(state, color) {
      state.color = color
    },
    setIsActivePlayer(state, active) {
      state.isActivePlayer = active
    },
    setIsCheckingMovement(state, active) {
      state.isCheckingMovement = active
    }
  }
}
