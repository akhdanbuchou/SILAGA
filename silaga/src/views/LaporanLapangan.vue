<template>
  <v-container
    fill-height
    fluid
    grid-list-xl
  >
    <v-layout
      justify-center
      wrap
    >
      <v-flex
        md12
      >
        <v-card>
          <v-card-title class="font-weight-medium">
            Daftar Laporan Lapangan Telegram
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Cari Laporan"
            ></v-text-field>
            <v-icon>mdi-magnify</v-icon>
          </v-card-title>
          <v-progress-circular v-if="telegram.length == 0" class="mb-3 ml-3"
              row wrap align-center justify-center
              :width="3"
              color="green"
              indeterminate
          ></v-progress-circular>
          <v-data-table v-else
            :headers="headers"
            :items="laporanTelegram"
            :search="search"
          >
            <template slot="items" slot-scope="props">
              <td class="text-xs-left">{{ props.item.pelapor }}</td>
              <td class="text-xs-left">{{ props.item.isi }}</td>
              <td class="text-xs-left">{{ props.item.kategori }}</td>
              <td class="text-xs-left">{{ props.item.timestamp }}</td>
            </template>
            <v-alert slot="no-results" :value="true" color="error" icon="mdi-warning">
              Your search for "{{ search }}" found no results.
            </v-alert>
          </v-data-table>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data: () => ({
    iteratorId: 1,
    search: '',
    headers: [
      { text: 'Pelapor', value: 'pelapor' },
      { text: 'Isi', value: 'content' },
      { text: 'Kategori', value: 'kategori' },
      { text: 'Waktu Lapor', value: 'timestamp' }
    ]
  }),
  computed:{
      ...mapGetters({
          telegram:'getTelegramReport'
      }),
      laporanTelegram(){
        var result = []
        var tempResult
        for(var i = 0; i< this.telegram.length; i++){
          var tempKategori = ""
          var toLoopKategori = this.telegram[i].kategori

          for(var j = 0; j < toLoopKategori.length; j++){
              if(toLoopKategori.length - j == 1){
                tempKategori += this.telegram[i].kategori[j]
              }else{
                tempKategori += this.telegram[i].kategori[j] + " - "
              }
          }
          tempResult = {
            pelapor: this.telegram[i].pelapor,
            kategori: tempKategori,
            timestamp: this.telegram[i].timestamp,
            isi: this.telegram[i].content
          }
          result.push(tempResult)

        }
        return result
      }
    },
    beforeMount(){
      this.$store.dispatch('getTelegramReport')
    }
}
</script>
