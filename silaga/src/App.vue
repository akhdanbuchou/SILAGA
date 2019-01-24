<template>
  <v-app>
    <core-toolbar v-if="!loginPath"/>
    <core-drawer v-if="!loginPath"/>
    <core-view/>
  </v-app>
</template>

<script>
export default{
  data(){
    return{
    }
  },
  computed:{
    loginPath(){
      var currentRoute = this.$route.name
      if(currentRoute == 'Login'){
        return true
      }else {
        return false
      }
    }
  },
  beforeCreate() {
    if (!this.$session.exists()) {
      this.$router.push('/login')
    }
  }
}


</script>

<style lang="scss">
@import '@/styles/index.scss';


</style>
