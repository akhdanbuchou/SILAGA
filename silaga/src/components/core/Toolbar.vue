<template>
  <v-toolbar
    id="core-toolbar"

    flat
    prominent
    style="background: #eee;"
  >
    <div class="v-toolbar-title">
      <v-toolbar-title class="tertiary--text font-weight-bold">
        {{ title }}
      </v-toolbar-title>
    </div>
    <v-spacer />
    <v-toolbar-items>
      <v-flex
        align-center
        layout
      >
        <v-text class="tertiary--text font-weight-regular">
          Selamat Datang, {{user}}
        </v-text>
        <v-btn color="grey darken-3" class="ml-4" @click="logout()">
          Logout
        </v-btn>
      </v-flex>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>

import {
  mapMutations
} from 'vuex'

export default {
  data: () => ({
    title: null,
    responsive: false,
    responsiveInput: false
  }),

  watch: {
    '$route' (val) {
      if(val.path == "/") {
        this.title = "Dashboard Analisis"
      }else {
        this.title = val.name
      }
    }
  },
  mounted () {
    this.onResponsiveInverted()
    window.addEventListener('resize', this.onResponsiveInverted)
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.onResponsiveInverted)
  },
  computed:{
    user(){
      return this.$session.get('currentUser').username
    }
  },
  methods: {
    ...mapMutations('app', ['setDrawer', 'toggleDrawer']),
    onClickBtn () {
      this.setDrawer(!this.$store.state.app.drawer)
    },
    logout () {
      this.$session.destroy()
      this.$router.push('/login')
    },
    onResponsiveInverted () {
      if (window.innerWidth < 991) {
        this.responsive = true
        this.responsiveInput = false
      } else {
        this.responsive = false
        this.responsiveInput = true
      }
    }
  }
}
</script>

<style>
  #core-toolbar a {
    text-decoration: none;
  }
</style>
