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
              <v-flex xs9 sm9 md9>
                <v-text-field
                  v-model="search"
                  label="Cari Laporan"
                ></v-text-field>
              </v-flex>

            <v-dialog v-model="modalDetail" max-width="500px">
              <ModalDetailLaporan
              :selectedLaporan="selectedLaporan" 
              :modalDetail="modalDetail" v-on:closeDetail="closeDetail($event)"
              ></ModalDetailLaporan>
            </v-dialog>
          <v-flex xs6 sm6 md6>
            <v-autocomplete
              :loading="loading" :items="dropGangguan" v-model="filterGangguan" 
              cache-items flat hide-no-data hide-details
              label="Pilih Filter Gangguan" solo-inverted>
            </v-autocomplete>
          </v-flex>
          <v-flex xs6 sm6 md6>
              <v-menu :close-on-content-click="false" v-model="menuDate1" :nudge-right="40"
                lazy transition="scale-transition" offset-y full-width min-width="290px">
                <v-text-field slot="activator" v-model="filterTanggal" label="Pilih Filter Tanggal" readonly>
                </v-text-field>
                <v-date-picker dark v-model="filterTanggal" @input="menuDate1 = false"></v-date-picker>
              </v-menu>
          </v-flex>
          </v-card-title>
          <v-progress-circular v-if="telegram.length == 0" class="mb-3 ml-3"
              row wrap align-center justify-center
              :width="3"
              color="green"
              indeterminate
          ></v-progress-circular>
          <v-data-table v-else
            :headers="headers"
            :items="filterBy(laporanTelegram, filterGangguan, filterTanggal)"
            :search="search"
          >
            <template slot="items" slot-scope="props">
              <td class="text-xs-left">{{ props.index + 1 }}</td>
              <td class="text-xs-left">{{ props.item.pelapor }}</td>
              <td class="text-xs-left">{{ props.item.kategori }}</td>
              <td class="text-xs-left">{{ props.item.timestamp }}</td>
              <td class="text-xs-left">{{ conciseReport(props.item.isi) }}</td>
              <td class="justify-left pl-3 layout px-0">
                <v-icon 
                  small
                  class="mr-2"
                  @click="popDetail(props.item)"
                  color="blue"
                >mdi-feature-search-outline</v-icon>
              </td>
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

import ModalDetailLaporan from "@/components/utilities/laporan/ModalDetailLaporan.vue";

export default {
  components: {
    ModalDetailLaporan
  },
  data: () => ({
    loading: false,
    menuDate1: false,
    filterGangguan:'',
    filterTanggal:'',
    modalDetail: false,
    selectedLaporan: {},
    search: '',
    headers: [
      { text: 'No', value:'no'},
      { text: 'Pelapor', value: 'pelapor' },
      { text: 'Kategori', value: 'kategori' },
      { text: 'Waktu Lapor', value: 'timestamp' },
      { text: 'Isi', value: 'content' },
      { text: '', value: 'action'}
    ]
  }),
  methods:{
    popDetail(laporan){
      this.selectedLaporan = laporan
      this.modalDetail = true
    },
    closeDetail(event){
      this.modalDetail = event
    },
    conciseReport(text){
        var result = text.substring(0,120) + "..."
        return result
    },
    filterBy(list, filterGangguan, filterTanggal){
      if (filterTanggal == '') {
        if(filterGangguan == 'Semua'){
          return list
        }else{
          return list.filter(laporan => {
            return laporan.kategori.indexOf(filterGangguan) > -1
          })
        }
      
      } else if (filterGangguan == 'Semua') {
        return list.filter(laporan => {
          return (
            laporan.tanggal.indexOf(filterTanggal) > -1
          )
        })
      } else if(filterGangguan != 'Semua' && filterTanggal != ''){
        return list.filter(laporan => {
          return (
            laporan.kategori.indexOf(filterGangguan) > -1 &&
            laporan.tanggal.indexOf(filterTanggal) > -1
          )
        })
      }else{
        return list
      }
    },
  },
  computed:{
      ...mapGetters({
          telegram:'getTelegramReport',
          categories:'getCategories'
      }),
      dropGangguan(){
        var result = []
        var awal = {
          value: 'Semua',
          text: 'Semua'
        }
        result.push(awal)
        for(var i = 0; i < this.categories.length; i++){
            var temp = {
                value: this.categories[i].kategori,
                text: this.categories[i].kategori
            }
            result.push(temp)
        }
        return result
      },
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
            id: this.telegram[i].id,
            pelapor: this.telegram[i].pelapor,
            kategori: tempKategori,
            timestamp: this.telegram[i].timestamp,
            tanggal: this.telegram[i].timestamp.substring(0,10),
            isi: this.telegram[i].content
          }
          result.push(tempResult)

        }
        return result
      }
    },
    beforeMount(){
      this.$store.dispatch('getTelegramReport')
      this.$store.dispatch('getAllCategories')
    }
}
</script>
