<template>
	<div>
	</div>
</template>

<script>
export default {
  name: 'LogOut',
  created() {
    // Change title of page
    document.title = 'Log out'

    // Log out
    this.$store.dispatch('logOut')

    // Go to the home page
    this.$router.push('/')
  }
}
</script>

<style scoped>
</style>
