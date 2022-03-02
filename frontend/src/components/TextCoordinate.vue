<template>
  <text :x="x_value" :y="y_value" :style="style">{{ value }}</text>
</template>

<script>
export default {
  name: 'TextCoordinate',
  props: {
    props_style: {
      boardSize: Number,
      x: Number,
      y: Number,
      color: String,
      value: String
    }
  },
  data() {
    return {
      x_value: this.props_style.x + '%',
      y_value: this.props_style.y + '%',
      style: {
        fontSize: 22.232 / this.props_style.boardSize + 'vmin',
        fontWeight: 600,
        fill: this.props_style.color == 'light' ? '#779952' : '#edeed1',
        userSelect: 'none'
      },
      value: this.props_style.value
    }
  }
}
</script>

<style>
</style>
