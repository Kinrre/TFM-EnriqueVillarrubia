<template>
    <tr>
      <td>{{ name }}</td>
      <td>{{ author }}</td>
      <td>{{ boardSize }}</td>
      <td>{{ maxMovements }}</td>
      <td>{{ is_training }}</td>
      <td>{{ is_trained }}</td>
      <td><button v-on:click="trainGame" type="button" class="transparent" :disabled=!training_available>{{ training_emoji }}</button></td>
      <td><button v-on:click="getRules" type="button" class="transparent">❓</button></td>
      <td><button v-on:click="createRoom" type="button" class="transparent">▶️</button></td>
    </tr>
</template>

<script>
export default {
  name: 'ProfileGame',
  props: {
    props_style: {
      id: Number,
      name: String,
      author: String,
      boardSize: Number,
      maxMovements: Number,
      is_training: Boolean,
      is_trained: Boolean,
      initial_board: String,
      pieces: Array
    }
  },
  data() {
    return {
      id: this.props_style.id,
      name: this.props_style.name,
      author: this.props_style.username,
      boardSize: this.props_style.board_size + 'x' + this.props_style.board_size,
      maxMovements: this.props_style.maximum_movements,
      is_training: this.props_style.is_training ? "✔️" : "❌",
      is_trained: this.props_style.is_trained ? "✔️" : "❌",
      training_available: !this.props_style.is_training && !this.props_style.is_trained,
      training_emoji: this.getTrainingEmoji(),
      initialBoard: this.props_style.initial_board,
      pieces: this.props_style.pieces
    }
  },
  methods: {
    getRules() {
      var pieces = ''

      for (let i = 0; i < this.pieces.length; i++) {
        let piece = this.pieces[i]
        pieces += 'Piece: ' + this.capitalize(piece.name)
        pieces += ' (' + piece.fen_name + ')</br>'

        for (let j = 0; j < piece.movements.length; j++) {
          let movement = piece.movements[j]
          pieces += this.capitalize(movement.direction) + ': ' + movement.range + ' '
        }

        pieces += '</br>'
      }

      var body = 'Initial board: ' + this.initialBoard + '<br/>' + pieces
      this.$swal('Rules', body, 'info')
    },
    getTrainingEmoji() {
      var emoji = "-"

      if (!this.props_style.is_training && !this.props_style.is_trained) {
        emoji = "🏋️"
      }
      
      return emoji
    },
    async trainGame() {
      await this.$store.dispatch('trainGame', this.id)

      if (this.$store.getters.isTrainingSuccessful) {
        this.is_training = "✔️"
        this.training_available = false
        this.training_emoji = '-'
      }
    },
    async createRoom() {
      // Create a room to play
      var authHeader = this.$store.getters.getAuthHeader
      var payload = {'gameId': this.id, 'authHeader': authHeader}
      await this.$store.dispatch('createRoom', payload)

      if (this.$store.getters.isAuthenticated) {
        await this.redirectToRoom()
      }
    },
    async redirectToRoom() {
      // Redirect to the room created
      var room = {
        name: 'Room',
        path: '/room/' + this.$store.getters.getRoomCode,
        params: {
          'roomCode': this.$store.getters.getRoomCode,
          'boardSize': this.$store.getters.getBoardSize,
          'initialBoard': this.$store.getters.getInitialBoard
        }
      }

      var title = ''
      var body = ''

      if (this.props_style.is_trained) {
        title = 'Player generated available!'
        body = 'Do you want to play with the generated player?'

        var response = await this.$swal({
          title: title,
          text: body,
          icon: 'question',
          showCancelButton: true
        })

        if (response.isConfirmed) {
          var payload = {
            'id': this.$store.getters.getGameId,
            'room_code': this.$store.getters.getRoomCode,
          }

          await this.$store.dispatch('createPlayer', payload)
        } else {
          this.createRoomLink()
        }
      } else {
        this.createRoomLink()
      }

      this.$router.push(room)
    },
    createRoomLink() {
      var title = 'Send your friends this link!'
      var body = 'http://localhost:8080/join-room/' + this.$store.getters.getRoomCode

      this.$swal(title, body)
    },
    capitalize(word) {
      const lower = word.toLowerCase();
      return word.charAt(0).toUpperCase() + lower.slice(1);
    }
  }
}
</script>

<style>
.transparent {
  background-color: transparent;
  background-repeat: no-repeat;
  border: none;
  overflow: hidden;
  outline: none;
}
</style>
