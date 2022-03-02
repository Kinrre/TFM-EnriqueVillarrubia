<template>
  <div class="movement-form">
    <h2 class="subtitle">Movements</h2>
    <div class="item-form">
      <div>
        <label for="north">Range north [Optional]</label>
      </div>
      <input type="number" placeholder="North" v-bind:id=north min="0">
    </div>
    <div class="item-form">
      <div>
        <label for="west">Range west [Optional]</label>
      </div>
      <input type="number" placeholder="West" v-bind:id=west min="0">
    </div>
    <div class="item-form">
      <div>
        <label for="east">Range east [Optional]</label>
      </div>
      <input type="number" placeholder="East" v-bind:id=east min="0">
    </div>
    <div class="item-form-double">
      <div>
        <label for="south">Range south [Optional]</label>
      </div>
      <input type="number" placeholder="South" v-bind:id=south min="0">
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovementForm',
  props: {
    props_style: {
      id: Number
    }
  },
  data() {
    return {
      id: this.props_style.id,
      north: `north-${this.props_style.id}`,
      west: `west-${this.props_style.id}`,
      east: `east-${this.props_style.id}`,
      south: `south-${this.props_style.id}`
    }
  },
  methods: {
    getData() {
      // Get the data from the movement
      var north = document.getElementById(this.north).value || '0'
      var west = document.getElementById(this.west).value || '0'
      var east = document.getElementById(this.east).value || '0'
      var south = document.getElementById(this.south).value || '0'

      var movement = `"movements": [
                        {
                          "direction": "north",
                          "range": ${north}
                        },
                        {
                          "direction": "west",
                          "range": ${west}
                        },
                        {
                          "direction": "east",
                          "range": ${east}
                        },
                        {
                          "direction": "south",
                          "range": ${south}
                        }
                      ]`

      return movement
    }
  }
}
</script>

<style>
</style>
