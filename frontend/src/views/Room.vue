<template>
  <div class="room">
    <Board :boardSize="boardSize" :initialBoard="initialBoard"/>
  </div>
</template>

<script>
import Board from '../components/Board.vue'

export default {
  name: 'Room',
  components: {
    Board
  },
  computed: {
    boardSize() {
      return this.$route.params.boardSize
    },
    initialBoard() {
      return this.$route.params.initialBoard
    },
  },
  methods: {
    movePiece(position) {
      // Move the piece to the new position obtain from the socket.io
      var board = this.$children[0]
      var pieces = board.$children

      // Index zero are the coordinates, so we start in the index one
      for (var i = 1; i < pieces.length; i++) {
        var piece = pieces[i]

        // Only move the piece in the 'fromPosition' to 'toPosition'
        if (position.fromPosition == piece.getStyle().transform) {
          piece.getStyle().transform = position.toPosition
          
          let hasCaptured = piece.capturePiece(true)
          piece.playSound(hasCaptured)
        }
      }
    },
    checkEndGame() {
      // Check if the game has finished (no more 'white' or 'black' pieces)
      var board = this.$children[0]
      var pieces = board.$children

      var color = this.$store.getters.getColor
      var isEndGame = true

      // Index zero are the coordinates, so we start in the index one
      for (var i = 1; i < pieces.length; i++) {
        var piece = pieces[i]
        
        if (color != piece.getColor()) {
          isEndGame = false
        }
      }

      // Emit a 'end_game' event
      var data = {
        'roomCode': this.$route.params.roomCode,
        'winner': color
      }

      if (isEndGame) {
        this.$socket.emit('end_game', data)
      }
    }
  },
  sockets: {
    connect() {
      var color = this.$store.getters.getColor
      var roomCode = this.$route.params.roomCode
      this.$socket.emit('join', roomCode)

      if (color == 'black') {
        var data = {'roomCode': roomCode, 'playerName': this.$route.params.playerName}
        this.$socket.emit('room_completed', data)
      }
    },
    roomCompleted(playerName) {
      var color = this.$store.getters.getColor

      if (color == 'white') {
        this.$store.commit('setIsActivePlayer', true)
        
        let title = playerName + ' has joined the game!'
        let body = 'Now you can move white pieces.'
        this.$swal(title, body, 'success')
      } else if (color == 'black') {
        let title = 'You have joined the game!'
        let body = 'You are the black pieces.'
        this.$swal(title, body, 'success') 
      }
    },
    move(position) {
      // Change the turn for the active player
      if (this.$store.getters.isActivePlayer) {
        this.$store.commit('setIsActivePlayer', false)
        
        // Check if the game has finished
        this.checkEndGame()
        return
      }

      // Change the turn for the NOT active player
      this.$store.commit('setIsActivePlayer', true)

      // Move the piece to the new position
      this.movePiece(position)
    },
    endGame(data) {
      var color = this.$store.getters.getColor

      if (color == data.winner) {
        let title = 'You win!'
        let body = 'Well played.'
        this.$swal(title, body, 'success')
      } else {
        let title = 'You loose!'
        let body = 'Good luck next time.'
        this.$swal(title, body, 'error')
      }
    }
  },
  created() {
    // Ensure the room has been properly created
    if (this.boardSize == null || this.initialBoard == null) this.$router.push('/')

    // Change title of page
    document.title = 'Room'
  },
  mounted() {
    this.$store.commit('setIsActivePlayer', false)
    this.$store.commit('setIsCheckingMovement', false)
    this.$socket.connect()
  },
  beforeDestroy() {
    var roomCode = this.$store.getters.getRoomCode
    this.$socket.emit('leave', roomCode)

    this.$socket.disconnect()
  }
}
</script>

<style>
</style>
