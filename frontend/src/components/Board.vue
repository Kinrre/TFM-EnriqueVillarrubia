<template>
  <div :style="style">
    <Coordinates :boardSize="boardSize"/>
    <Piece v-for="piece in pieces" v-bind:id="piece.id" v-bind:boardSize="boardSize" v-bind:props_style="piece" :key="piece.id"/>
  </div>
</template>

<script>
import Coordinates from './Coordinates.vue'
import Piece from './Piece.vue'

export default {
  name: 'Board',
  components: {
    Coordinates,
    Piece
  },
  props: {
    boardSize: Number,
    initialBoard: String
  },
  data() {
    return {
      style: {
        height: 'auto',
        width: '100%',
        position: 'relative',
        margin: 'auto',
        backgroundImage: this.getBoard(),
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'contain',
        userSelect: 'none'
      },
      pieces: this.piecesFromFen()
    }
  },
  methods: {
    onResize() {
      // Ensure the div is a perfect square
      if (innerHeight > innerWidth) {
        this.style.height = innerWidth + 'px'
        this.style.width = innerWidth + 'px'
      } else {
        this.style.height = innerHeight + 'px'
        this.style.width = innerHeight + 'px'
      }
    },
    isLower(character) {
      // Check if a character is lowercase
      return (character === character.toLowerCase()) && (character !== character.toUpperCase())
    },
    getBoard() {
      // Get the board background image
      return 'url(' + require('@/assets/boards/' + this.boardSize + 'x' + this.boardSize + '_board.png') + ')'
    },
    getFen() {
      // Get the fen from the actual pieces
      var fen = ''
      var pieces = this.$children

      for (let height = 0; height < this.boardSize; height++) {
        for (let width = 0; width < this.boardSize; width++) {
          let width_style = width * 100
          let height_style = height * 100
          let fen_piece = '1'

          // Index zero are the coordinates, so we start in the index one
          for (let i = 1; i < pieces.length; i++) {
            let piece = pieces[i]
            let position = piece.getFromPosition()

            // Get position if fromPosition is not available
            if (position == null) {
              position = piece.getPosition()
            }

            // Check if there is a piece in that position
            if (position[0] == width_style && position[1] == height_style) {
              fen_piece = piece.getFenName()
            }
          }
          
          fen += fen_piece
        }
        fen += '/'
      }

      // Remove the last '/'
      fen = fen.slice(0, -1)

      return fen
    },
    piecesFromFen() {
      // Create pieces components from a fen string
      var pieces = []
      var row = 0, column = 0, id = 0

      for (let piece_type = 0; piece_type < this.initialBoard.length; piece_type++) {
        var piece = {}, char_piece
        char_piece = this.initialBoard.charAt(piece_type)
        
        if (parseInt(char_piece)) {
          column += parseInt(char_piece)
        } else if (char_piece == '/') {
          row += 1
          column = 0
        } else {
          piece.id = id
          piece.piece = char_piece
          piece.color = this.isLower(char_piece) ? 'black' : 'white'
          piece.size = 100 / this.boardSize
          piece.offsetX = 100 * column
          piece.offsetY = 100 * row
          pieces.push(piece)

          column += 1
          id += 1
        }
      }

      return pieces
    },
    removePiece(index) {
      // Remove a piece given his index
      this.pieces.splice(index, 1)
    }
  },
  mounted() {
    window.addEventListener('resize', this.onResize)
    
    // Resize first time
    this.onResize()
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize)
  }
}
</script>

<style>
</style>
