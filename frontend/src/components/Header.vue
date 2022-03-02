<template>
    <div v-if="!isAuthenticated" class="login-register">
      <router-link to="/">Home</router-link>
      <router-link to="/register/" class="register">Register</router-link>
      <router-link to="/login/">Login</router-link>
    </div>
    <div v-else class="login-register">
      <router-link to="/">Home</router-link>
      <router-link to="/profile/" class="register">Username - {{ username }}</router-link>
      <router-link to="/log-out/">Log out</router-link>
    </div>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      username: this.$store.getters.getUsername,
      isAuthenticated: this.$store.getters.isAuthenticated
    }
  }
}
</script>

<style scoped>
.login-register {
  width: 80%;
  font-size: 1.75vmin;
  margin-top: 0.5%;
  display: flex;
  justify-content: flex-end;
}

.register {
  margin-left: auto;
  margin-right: 2%;
}
</style>
