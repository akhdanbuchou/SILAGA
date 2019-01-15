<template>
  <v-app>
    <core-filter v-if="!loginPath"/>
    <core-toolbar v-if="!loginPath"/>
    <core-drawer v-if="!loginPath"/>
    <core-view/>
  </v-app>
</template>

<script>
export default{
  computed:{
    loginPath(){
      var currentRoute = this.$route.name
      if(currentRoute == 'Login'){
        return true
      }else {
        return false
      }
    }
  }
}


</script>

<style lang="scss">
@import '@/styles/index.scss';


</style>
