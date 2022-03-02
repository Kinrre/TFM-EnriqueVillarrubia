<template>
  <div class="login">
    <h1 class="header">Login</h1>
    <form @submit="login" class="form-login" method="post">
      <div class="item-form">
        <div>
          <label for="username">Username</label>
        </div>
        <input type="text" placeholder="Username" id="username" required="required">
      </div>
      <div class="item-form-double">
        <div>
          <label for="password">Password</label>
        </div>
        <input type="password" placeholder="Password" id="password" required="required">
      </div>
      <div class="item-form">
         <input type="submit" value="Login" id="login">
      </div>
      <div class="item-form-bottom">
        <router-link to="/register/">New? Register now!</router-link>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Login',
  methods: {
    async login(e) {
      // Prevent default behaviour of submit
      e.preventDefault()

      var credentials = this.getCredentials()

      await this.$store.dispatch('login', credentials)

      if (this.$store.getters.isAuthenticated) {
        // Go to the home page
        this.$router.push('/profile/')
      }
    },
    getCredentials() {
      // Get the credentials from the user
      var username = this.capitalize(document.getElementById('username').value)
      var password = document.getElementById('password').value
      return {'username': username, 'password': password}
    },
    capitalize(word) {
      const lower = word.toLowerCase();
      return word.charAt(0).toUpperCase() + lower.slice(1);
    }
  },
  created() {
    // Change title of page
    document.title = 'Login'
  }
}
</script>

<style scoped>
.login {
  height: 100vh;
  display: flex;
  align-items: center;
  flex-direction: column;
  margin: auto;
}

.header {
  margin-top: 35vh;
  margin-bottom: 2vh;
  font-size: 3.5vmin;
}

.form-login {
  font-size: 1.75vmin;
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
