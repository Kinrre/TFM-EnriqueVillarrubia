<template>
  <div class="profile">
    <Header/>
    <h1 class="header-title-profile">Your Games</h1>
    <div class="new-game">
      <router-link to="/new-game/">➕ New Game</router-link>
    </div>
    <div class="games">
      <table class="table-games">
        <tr>
          <th>Name</th>
          <th>Author</th>
          <th>Board size</th>
          <th>Max Moves</th>
          <th>Is Training</th>
          <th>Is Trained</th>
          <th>Train</th>
          <th>Rules</th>
          <th>Play</th>
        </tr>
        <ProfileGame v-for="game in games" v-bind:props_style="game" :key="game.id"/>
      </table>
    </div>
    <div v-if="!isGamesLoaded">
      <h3>Loading please wait...</h3>
    </div>
  </div>
</template>

<script>
import Header from '../components/Header.vue'
import ProfileGame from '../components/ProfileGame.vue'

export default {
  name: 'Profile',
  components: {
    Header,
    ProfileGame
  },
  data() {
    return {
      games: this.getMeGames(),
      isGamesLoaded: false
    }
  },
  methods: {
    async getMeGames() {
      await this.$store.dispatch('getMeGames')
      this.games = this.$store.getters.getGames
      this.isGamesLoaded = true
    }
  },
  created() {
    // Change title of page
    document.title = 'Profile'
  }
}
</script>

<style>
.profile {
  height: 100vh;
  display: flex;
  align-items: center;
  flex-direction: column;
}

.header-title-profile {
  margin-bottom: 0%;
  font-size: 3.5vmin;
}

.new-game {
  width: 80%;
  font-size: 1.75vmin;
  margin-top: 0.5%;
  display: flex;
  justify-content: flex-end;
}

.games {
  width: 80%;
  overflow-x: auto;
  margin-bottom: 2%;
}

.table-games {
  width: 100%;
  font-size: 1.75vmin;
  text-align: center;
  border-collapse: separate;
  border-spacing: 0 0.5em;
}

.table-games tr:nth-child(even) {
  background-color: #779556;
  color: black;
}

.table-games tr:nth-child(2n+3) {
  background-color: #ebecd0;
  color: black;
}

.table-games tr:nth-child(even):hover {
  color: #ebecd0;
}

.table-games tr:nth-child(2n+3):hover {
  color: #779556;
}
</style>
