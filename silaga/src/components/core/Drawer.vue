<template>
  <v-navigation-drawer
    id="app-drawer"
    v-model="inputValue"
    app
    dark
    floating
    persistent
    mobile-break-point="991"
    width="260"
  >
    <v-layout
      class="fill-height"
      tag="v-list"
      column
    >
      <v-list-tile avatar>
        <v-list-tile-avatar
          color="white"
        >
          <v-img
            :src="logo"
            height="60"
            contain
          />
        </v-list-tile-avatar>
        <v-list-tile-title class="title">
          SILAGA
        </v-list-tile-title>
      </v-list-tile>
      <v-divider/>
      <v-list-tile
        v-if="responsive"
      >
        <v-text-field
          class="purple-input search-input"
          label="Search..."
          color="purple"
        />
      </v-list-tile>
      <!--<v-list-tile
        v-for="(link, i) in links"
        :key="i"
        :to="link.to"
        :active-class="color"
        avatar
        class="v-list-item"
      >
        <v-list-tile-action>
          <v-icon>{{ link.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-title
          v-text="link.text"
        />
      </v-list-tile>-->
      <v-list-tile
      to="/" :active-class="color" avatar class="v-list-item">
        <v-list-tile-action>
          <v-icon>mdi-home</v-icon>
        </v-list-tile-action>
        <v-list-tile-title>Beranda</v-list-tile-title>
      </v-list-tile>

      <v-list-tile v-if="this.$session.get('currentUser').berita_config == '1'"
      to="/detail-berita" :active-class="color" avatar class="v-list-item">
        <v-list-tile-action>
          <v-icon>mdi-newspaper</v-icon>
        </v-list-tile-action>
        <v-list-tile-title>Daftar Berita</v-list-tile-title>
      </v-list-tile>

      <v-list-tile v-if="this.$session.get('currentUser').access_report == '1'"
      to="/laporan-lapangan" :active-class="color" avatar class="v-list-item">
        <v-list-tile-action>
          <v-icon>mdi-telegram</v-icon>
        </v-list-tile-action>
        <v-list-tile-title>Berita Lapangan</v-list-tile-title>
      </v-list-tile>

      <v-list-tile v-if="this.$session.get('currentUser').user_config == '1'"
      to="/konfigurasi" :active-class="color" avatar class="v-list-item">
        <v-list-tile-action>
          <v-icon>mdi-settings</v-icon>
        </v-list-tile-action>
        <v-list-tile-title>Konfigurasi Sistem</v-list-tile-title>
      </v-list-tile>
    </v-layout>
  </v-navigation-drawer>
</template>

<script>
// Utilities
import {
  mapMutations,
  mapState
} from 'vuex'

export default {
  data: () => ({
    logo: './img/silaga-logo.png',
    links: [
      {
        to: '/',
        icon: 'mdi-home',
        text: 'Beranda'
      },
      {
        to: '/detail-berita',
        icon: 'mdi-newspaper',
        text: 'Detail Berita'
      },
      {
        to: '/laporan-lapangan',
        icon: 'mdi-telegram',
        text: 'Laporan Lapangan'
      },
      {
        to: '/konfigurasi',
        icon: 'mdi-settings',
        text: 'Konfigurasi Sistem'
      }
    ],
    responsive: false
  }),
  computed: {
    ...mapState('app', ['image', 'color']),
    inputValue: {
      get () {
        return this.$store.state.app.drawer
      },
      set (val) {
        this.setDrawer(val)
      }
    },
    items () {
      return this.$t('Layout.View.items')
    }
  },
  mounted () {
    this.onResponsiveInverted()
    window.addEventListener('resize', this.onResponsiveInverted)
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.onResponsiveInverted)
  },
  methods: {
    ...mapMutations('app', ['setDrawer', 'toggleDrawer']),
    onResponsiveInverted () {
      if (window.innerWidth < 991) {
        this.responsive = true
      } else {
        this.responsive = false
      }
    }
  }
}
</script>

<style lang="scss">
  #app-drawer {
    .v-list__tile {
      border-radius: 4px;

      &--buy {
        margin-top: auto;
        margin-bottom: 17px;
      }
    }

    .v-image__image--contain {
      top: 9px;
      height: 60%;
    }

    .search-input {
      margin-bottom: 30px !important;
      padding-left: 15px;
      padding-right: 15px;
    }
  }
</style>
