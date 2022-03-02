<template>
  <div :style="style"></div>
</template>

<script>
export default {
  name: 'Piece',
  props: {
    id: Number,
    boardSize: Number,
    props_style: {
      piece: String,
      color: String,
      size: Number,
      offsetX: Number,
      offsetY: Number
    }
  },
  data() {
    return {
      dragging: false,
      fromPosition: null,
      toPosition: null,
      style: {
        height: this.props_style.size + '%',
        width: this.props_style.size + '%',
        position: 'absolute',
        transform: 'translate(' + this.props_style.offsetX + '%, ' + this.props_style.offsetY + '%)',
        backgroundImage: this.getPiece(),
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'contain',
        userSelect: 'none',
        willChange: 'transform', // Performance boost
        cursor: 'grab'
      }
    }
  },
  methods: {
    onMouseDown(event) {
      // Ensure is the active player
      if (!this.$store.getters.isActivePlayer) return

      // Ensure we are not checking a movement
      if (this.$store.getters.isCheckingMovement) return

      // Ensure is the right color
      if (this.$store.getters.getColor != this.props_style.color) return 

      // Ensure we only execute in the clicked component
      if (!event.target.__vue__) return
      if (event.target.__vue__._uid != this._uid) return

      // Change the cursor to grab and tell that we are grabbing the piece
      this.dragging = true
      this.style.cursor = 'grabbing'

      // Save original position
      this.savePosition('fromPosition')

      // Center the piece into the cursor
      this.movePiece(event)
    },
    onMouseMove(event) {
      // Ensure is the active player
      if (!this.$store.getters.isActivePlayer) return

      // Ensure we are not checking a movement
      if (this.$store.getters.isCheckingMovement) return

      // Ensure is the right color
      if (this.$store.getters.getColor != this.props_style.color) return 

      // Ensure we are dragging the component
      if (!this.dragging) return

      // Move the piece
      this.movePiece(event)
    },
    async onMouseUp() {
      // Ensure is the active player
      if (!this.$store.getters.isActivePlayer) return

      // Ensure we are not checking a movement
      if (this.$store.getters.isCheckingMovement) return

      // Ensure is the right color
      if (this.$store.getters.getColor != this.props_style.color) return 

      // Ensure we are dragging the component
      if (!this.dragging) return

      // Undo the cursor and tell that we are not grabbing the piece
      this.dragging = false
      this.style.cursor = 'grab'

      // Center the piece into a square
      this.centerPiece()

      // Save the new position
      this.savePosition('toPosition')

      // Check only if a piece has been captured
      var hasCaptured = this.capturePiece(false)

      // Play the corresponded sound
      this.playSound(hasCaptured)

      // Emit 'move' event if the new position is different and valid
      var isValid = await this.emitMove()

      // Delete the piece in the same square (capture the piece) if is valid
      if (isValid) {
        this.capturePiece(true)
      }
    },
    savePosition(type) {
      // Save the coordinates of the piece
      var coordinates = this.getPosition()

      if (type == 'fromPosition') {
        this.fromPosition = coordinates
      } else if (type == 'toPosition') {
        this.toPosition = coordinates
      }
    },
    movePiece(event) {
      // Ensure that we have a parent element
      if (!event.target.parentElement) return

      // Get the bounds of the board
      var boardBounds = event.target.parentElement.getBoundingClientRect()

      // Calculate the new raw offsets positions centering the piece into the mouse
      var rawOffsetX = event.clientX - boardBounds.left - this.$el.clientWidth / 2
      var rawOffsetY = event.clientY - boardBounds.top - this.$el.clientHeight / 2

      // Left overflow bug prevention
      rawOffsetX = this.leftOverflow(event, rawOffsetX)

      // Calculating the new relative offsets
      var offsetX = rawOffsetX * 100 / this.$el.clientWidth
      var offsetY = rawOffsetY * 100 / this.$el.clientHeight

      // Ensure that we are not outside the limits of the board
      var checkedOffsets = this.checkBounds(offsetX, offsetY)
      offsetX = checkedOffsets[0]
      offsetY = checkedOffsets[1]

      // Update the position
      this.style.transform = 'translate(' + offsetX + '%, ' + offsetY + '%)'
    },
    leftOverflow(event, rawOffsetX) {
      // Checking if we outside the board in the left part and correct it
      var marginLeft = window.getComputedStyle(this.$parent.$el).getPropertyValue('margin-left')
      marginLeft = parseInt(marginLeft)

      if (event.clientX < marginLeft) {
        rawOffsetX = 0
      }

      return rawOffsetX
    },
    checkBounds(offsetX, offsetY) {
      // Check the bounds of the board size
      var limit = 100 * (this.boardSize - 1)

      // Check the X axis
      if (offsetX > limit) {
        offsetX = limit
      } else if (offsetX < 0) {
        offsetX = 0
      }
      
      // Check the Y axis
      if (offsetY > limit) {
        offsetY = limit
      } else if (offsetY < 0) {
        offsetY = 0
      }

      return [offsetX, offsetY]
    },
    centerPiece() {
      // Correct the position of a piece centering in a square
      var offsets = this.getPosition()
      var offsetX = offsets[0]
      var offsetY = offsets[1]

      offsetX = Math.round(offsetX / 100) * 100
      offsetY = Math.round(offsetY / 100) * 100

      // Update the position
      this.style.transform = 'translate(' + offsetX + '%, ' + offsetY + '%)'
    },
    capturePiece(isValid) {
      // Get the component children of the board
      var children = this.$parent.$children
      var hasCaptured = false

      // Index zero are the coordinates, so we start in the index one
      for (var i = 1; i < children.length; i++) {
        var child = children[i]

        // The position is the same and the component is different
        if (this._uid != child._uid && this.getStyle().transform == child.getStyle().transform) {
          if (isValid) {
            this.$parent.removePiece(i - 1)
          }
          hasCaptured = true
        }
      }

      return hasCaptured
    },
    playSound(hasCaptured) {
      // Play different sound depending if the piece has captured another piece or not
      var audio

      if (hasCaptured) {
        audio = new Audio(require('@/assets/sounds/capture.webm'))
      } else if (this.props_style.color == "white") {
        audio = new Audio(require('@/assets/sounds/move-self.webm'))
      } else if (this.props_style.color == "black") {
        audio = new Audio(require('@/assets/sounds/move-opponent.webm'))
      }

      audio.play()
    },
    playIllegalSound() {
      // Play an illegal sound due to an invalid movement
      var audio = new Audio(require('@/assets/sounds/illegal.webm'))
      audio.play()
    },
    async emitMove() {
      // Emit 'move' event if the new position is different
      let isValid = true
      
      if (this.fromPosition[0] != this.toPosition[0] || this.fromPosition[1] != this.toPosition[1]) {
        // Unable the movement while waiting to confirm the validity of the movement
        this.$store.commit('setIsCheckingMovement', true)

        if (await this.isValidMovement()) {
          var fromPosition = 'translate(' + this.fromPosition[0] + '%, ' + this.fromPosition[1] + '%)'
          var toPosition = 'translate(' + this.toPosition[0] + '%, ' + this.toPosition[1] + '%)'
          var data = {
            'fromPosition': fromPosition,
            'toPosition': toPosition,
            'roomCode': this.$route.params.roomCode
          }
          this.$socket.emit('move', data)

          // Unset the fromPosition and toPosition
          this.fromPosition = null
          this.toPosition = null
        } else {
          // Undo the movement as is not valid
          isValid = false
          this.undoMovement()
        }

        // Unset the flag
        this.$store.commit('setIsCheckingMovement', false)
      }

      return isValid
    },
    async isValidMovement() {
      // Check if the movement is valid
      var gameId = this.$store.getters.getGameId
      var fen = this.$parent.getFen()
      var fromPosition = this.fromPosition
      var toPosition = this.toPosition

      var payload = {
        'id': gameId,
        'board': fen,
        'color': this.props_style.color,
        'from_position_x': fromPosition[1] / 100,
        'from_position_y': fromPosition[0] / 100,
        'to_position_x': toPosition[1] / 100,
        'to_position_y': toPosition[0] / 100
      }

      await this.$store.dispatch('checkMovement', payload)

      return this.$store.getters.isValidMovement
    },
    undoMovement() {
      // Undo the previous movement
      this.style.transform = 'translate(' + this.fromPosition[0] + '%, ' + this.fromPosition[1] + '%)'

      this.fromPosition = null
      this.toPosition = null

      this.playIllegalSound()
    },
    getPiece() {
      // Get the piece background image
      return 'url(' + require('@/assets/pieces/' + this.props_style.color + '/' + this.props_style.color + '_' + this.props_style.piece + '.png') + ')'
    },
    getFenName() {
      // Return the fen name of the piece
      return this.props_style.piece
    },
    getColor() {
      // Return the color of the piece
      return this.props_style.color
    },
    getStyle() {
      // Return the style of the piece
      return this.style
    },
    getFromPosition() {
      // Return the fromPosition of the piece
      return this.fromPosition
    },
    getPosition() {
      // Return the position of the piece
      return this.style.transform.match(/[+-]?\d+(\.\d+)?/g)
    }
  },
  mounted() {
    window.addEventListener('mousedown', this.onMouseDown)
    window.addEventListener('mousemove', this.onMouseMove)
    window.addEventListener('mouseup', this.onMouseUp)
  },
  beforeDestroy() {
    window.removeEventListener('mousedown', this.onMouseDown)
    window.removeEventListener('mousemove', this.onMouseMove)
    window.removeEventListener('mouseup', this.onMouseUp)
  }
}
</script>

<style>
</style>
