<template>
  <div class="new-game-container">
    <Header/>
    <h1 class="header-title-new-game">New Game</h1>
    <div class="new-game-form">
      <form @submit="createGame" id="game-form" method="post">
        <h2 class="subtitle">General information</h2>
        <div class="item-form">
          <div>
            <label for="name">Name</label>
          </div>
          <input type="text" placeholder="Name" id="name" required="required">
        </div>
        <div class="item-form">
          <div>
            <label for="board-size">Board size</label>
          </div>
          <input type="number" placeholder="Board size" id="board-size" min="1" required="required">
        </div>
        <div class="item-form">
          <div>
            <label for="initial-board">Initial board</label>
          </div>
          <input type="text" placeholder="Example: 1pp1/4/4/1PP1" id="initial-board" required="required">
        </div>
        <div class="item-form-double">
          <div>
            <label for="maximum-movements">Max moves</label>
          </div>
          <input type="number" placeholder="Max moves" id="maximum-movements" min="1" required="required">
        </div>
        <PieceForm v-for="piece in pieces" v-bind:props_style="piece" :key="piece.id"/>
        <div class="item-form-bottom">
          <input type="submit" value="Create game" id="create-game">
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import Header from '../components/Header.vue'
import PieceForm from '../components/PieceForm.vue'

export default {
  name: 'NewGame',
  components: {
    Header,
    PieceForm
  },
  data() {
    return {
      pieces: this.initPieces()
    }
  },
  methods: {
    initPieces() {
      // Initialize the pieces
      var pieces = [{'id': 0, 'buttonDisabled': true}]
      return pieces
    },
    addPieceForm() {
      // Add a piece form
      var piece = {'id': this.pieces.length, 'buttonDisabled': false}
      this.pieces.push(piece)
    },
    removePieceForm() {
      // Remove a piece form
      if (this.pieces != 1) {
        this.pieces.pop()
      }
    },
    async createGame(e) {
      // Prevent default behaviour of submit
      e.preventDefault()
      
      // Create a game from the data of the form
      var name = document.getElementById('name').value
      var boardSize = document.getElementById('board-size').value
      var initialBoard = document.getElementById('initial-board').value
      var maximumMovements = document.getElementById('maximum-movements').value
      
      var piecesForm = this.$children
      var piecesBody = ''

      // Index zero is the header, so we start in index one
      for (let i = 1; i < piecesForm.length; i++) {
        var pieceForm = piecesForm[i]
        piecesBody += pieceForm.getData() + ','
      }

      // Remove last ','
      piecesBody = piecesBody.slice(0, -1)

      var pieces = `"pieces": [
                      ${piecesBody}
                    ]`

      var game = `{
                    "name": "${name}",
                    "board_size": ${boardSize},
                    "initial_board": "${initialBoard}",
                    "maximum_movements": ${maximumMovements},
                    ${pieces}
                  }`

      // Create a JSON object
      var gameJSON = JSON.parse(game)

      // Create the game in the backend
      await this.$store.dispatch('createGame', gameJSON)
    }
  },
  created() {
    // Change title of page
    document.title = 'New Game'
  }
}
</script>

<style>
.new-game-container {
  height: 100vh;
  margin: auto;
  display: flex;
  align-items: center;
  flex-direction: column;
}

.header-title-new-game {
  margin-bottom: 2%;
  font-size: 3.5vmin;
}

.subtitle {
  font-size: 3vmin;
}

.new-game-form {
  width: 25%;
  font-size: 1.75vmin;
  overflow-x: auto;
  margin-bottom: 2%;
}

.item-form {
  width: 100%;
  margin-bottom: 1vh;
}

.item-form-double {
  margin-bottom: 2vh;
}

.item-form-bottom {
  margin-top: 2vh;
  text-align: center;
}

input {
  width: 100%;
}
</style>
