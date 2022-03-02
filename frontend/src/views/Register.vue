<template>
  <div class="register">
    <h1 class="header">Register</h1>
    <form @submit="register" class="form-register" method="post">
      <div class="item-form">
        <div>
          <label for="username">What is your username?</label>
        </div>
        <input type="text" placeholder="Username" id="username" required="required">
      </div>
      <div class="item-form-double">
        <div>
          <label for="password">Create your password</label>
        </div>
        <input type="password" placeholder="Password" id="password" required="required">
      </div>
      <div class="item-form">
         <input type="submit" value="Create account" id="register" class="register-submit">
      </div>
      <div class="item-form-bottom">
        <router-link to="/login/">Already have an account?</router-link>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Register',
  methods: {
    async register(e) {
      e.preventDefault() // Prevent default behaviour of submit

      var credentials = this.getCredentials()

      if (!credentials) {
        this.$swal('Missing values!', 'Check that you have filled all the fields.', 'warning')
        return
      }

      await this.$store.dispatch('register', credentials)
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
    document.title = 'Register'
  }
}
</script>

<style scoped>
.register {
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

.form-register {
  font-size: 1.75vmin;
}

.item-form {
  margin-bottom: 1vh;
}

.item-form-double {
  margin-bottom: 2vh;
}

.item-form-bottom {
  margin-top: 2vh;
  text-align: center;
}

.register-submit {
  width: 100%;
}

input {
  width: 100%;
}
</style>
