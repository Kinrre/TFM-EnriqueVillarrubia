<template>
  <div>
  </div>
</template>

<script>
export default {
  name: 'JoinRoom',
  methods: {
    async registerRoom() {
      var authHeader = this.$store.getters.getAuthHeader
      var roomCode = window.location.href.substring(window.location.href.lastIndexOf('/') + 1)
      var payload = {'roomCode': roomCode, 'authHeader': authHeader}
      await this.$store.dispatch('joinRoom', payload)
    },
    redirectToRoom() {
      // Redirect to the room created
      var room = {
        name: 'Room',
        path: '/room/' + this.$store.getters.getRoomCode,
        params: {
          'roomCode': this.$store.getters.getRoomCode,
          'boardSize': this.$store.getters.getBoardSize,
          'initialBoard': this.$store.getters.getInitialBoard,
          'playerName': this.$store.getters.getUsername
        }
      }

      this.$router.push(room)
    }
  },
  async mounted() {
    // Register room
    await this.registerRoom()

    // Go to the room
    if (this.$store.getters.isRoomCreated && this.$store.getters.isAuthenticated) {
      this.redirectToRoom()
    }
  }
}
</script>

<style>
</style>
