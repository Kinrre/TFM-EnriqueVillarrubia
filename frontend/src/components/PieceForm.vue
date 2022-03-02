<template>
  <div class="piece-form">
    <div class="piece-container">
      <h2 class="subtitle">Piece</h2>
      <button v-on:click="addPieceForm" class="piece-button" type="button">+ New piece</button>
      <button v-on:click="removePieceForm" :disabled=buttonDisabled class="piece-button" type="button">- Remove piece</button> 
    </div>
    <div class="item-form">
      <div>
        <label for="piece-name">Name</label>
      </div>
        <input type="text" placeholder="Name" v-bind:id=pieceName required="required">
      </div>
    <div class="item-form-double">
      <div>
        <label for="fen-name">Fen name</label>
      </div>
        <input type="text" placeholder="Fen name" v-bind:id=fenName maxlength="1" required="required">
    </div>
    <MovementForm v-bind:props_style="movement" :key="movement.id"/>
  </div>
</template>

<script>
import MovementForm from '../components/MovementForm.vue'

export default {
  name: 'PieceForm',
  components: {
    MovementForm
  },
  props: {
    props_style: {
      id: Number,
      buttonDisabled: Boolean
    }
  },
  data() {
    return {
      id: this.props_style.id,
      buttonDisabled: this.props_style.buttonDisabled,
      pieceName: `piece-name-${this.props_style.id}`,
      fenName: `fen-name-${this.props_style.id}`,
      movement: {'id': this.props_style.id}
    }
  },
  methods: {
    addPieceForm() {
      // Add a piece form
      this.$parent.addPieceForm()
    },
    removePieceForm() {
      // Remove a piece form
      this.$parent.removePieceForm()
    },
    getData() {
      // Get the data from the piece
      var name = document.getElementById(this.pieceName).value
      var fenName = document.getElementById(this.fenName).value
      var movement = this.$children[0].getData()

      var piece = `{
                    "name": "${name}",
                    "fen_name": "${fenName}",
                    ${movement}
                  }`

      return piece
    }
  }
}
</script>

<style>
.piece-container {
  display: flex;
  align-items: left;
  flex-direction: row;
  justify-content: flex-start;
}

.piece-button {
  margin-left: 2%;
}
</style>
