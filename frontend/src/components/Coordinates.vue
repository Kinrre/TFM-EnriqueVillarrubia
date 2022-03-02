<template>
  <svg viewbox="0 0 100 100" :style="style">
    <TextCoordinate v-for="text in texts" v-bind:props_style="text" :key="text.id"/>
  </svg>
</template>

<script>
import TextCoordinate from './TextCoordinate.vue'

export default {
  name: 'Coordinates',
  props: {
    boardSize: Number
  },
  components: {
    TextCoordinate
  },
  data() {
    return {
      style: {
        height: '100%',
        width: '100%',
        position: 'absolute'
      },
      texts: this.getTexts()
    }
  },
  methods: {
    getTexts() {
      // Create TextCoordinate components for the current board
      var texts = []

      for (let i = 0; i < this.boardSize; i++) {
        for (let j = 0; j < this.boardSize; j++) {
          // Numbers
          if (j == 0) {
            let text = {}
            text.boardSize = this.boardSize
            text.color = (i + j) % 2 == 0 ? 'light' : 'dark'
            text.x = 6 / this.boardSize
            text.y = 28 / this.boardSize + i * 100 / this.boardSize
            text.value = this.boardSize - i.toString()
            texts.push(text)
          } 
          
          // Letters
          if (i == this.boardSize - 1) {
            let text = {}
            text.boardSize = this.boardSize
            text.color = (i + j) % 2 == 0 ? 'light' : 'dark'
            text.x = 80 / this.boardSize + j * 100 / this.boardSize
            text.y = 99
            text.value = String.fromCharCode(97 + j)
            texts.push(text)
          }
        }
      }

      return texts
    }
  }
}
</script>

<style>
</style>
