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
            Daftar Analisis Berita Online
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
            <v-icon>mdi-magnify</v-icon>

            <ModalCreateBerita :categories="categories"></ModalCreateBerita>

            <v-dialog v-model="modalDetail" max-width="500px">
              <ModalDetailBerita 
              :selectedNews="selectedNews" 
              :modalDetail="modalDetail" v-on:closeDetail="closeDetail($event)"
              ></ModalDetailBerita>
            </v-dialog>
          
            <v-dialog v-model="modalEdit" max-width="500px">
              <ModalUpdateBerita 
              :categories="categories"
              :selectedNews="selectedNews" 
              :modalEdit="modalEdit" v-on:closeEdit="closeEdit($event)"
              ></ModalUpdateBerita>
            </v-dialog>
            
          
          </v-card-title>
          <v-progress-circular v-if="news.length == 0" class="mb-3 ml-3"
              row wrap align-center justify-center
              :width="3"
              color="green"
              indeterminate
            ></v-progress-circular>
          <v-data-table v-else
            :headers="headers"
            :items="berita"
            :search="search"
          >
            <template slot="items" slot-scope="props">
              <td class="text-xs-left">{{ props.index + 1 }}</td>
              <td class="text-xs-left">{{ props.item.title }}</td>
              <td class="text-xs-left">{{ props.item.kategori3 }}</td>
              <td class="text-xs-left">{{ props.item.lokasi }}</td>
              <td class="text-xs-left">{{ props.item.waktu }}</td>
              <td class="text-xs-left">{{ conciseNews(props.item.isi) }}</td>
              <td class="justify-left pl-3 layout px-0">
                <v-icon
                  small
                  class="mr-2"
                  @click="popDetail(props.item)"
                  color="blue"
                >
                  mdi-feature-search-outline
                </v-icon>
                <v-icon
                  small
                  class="mr-2"
                  @click="popEdit(props.item)"
                  color="green"
                >
                  mdi-pencil
                </v-icon>
                <!--<v-icon
                  small
                  @click="popDelete(props.item)"
                >
                  mdi-delete
                </v-icon>-->
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

import ModalCreateBerita from "@/components/utilities/berita/ModalCreateBerita.vue";
import ModalDetailBerita from "@/components/utilities/berita/ModalDetailBerita.vue";
import ModalUpdateBerita from "@/components/utilities/berita/ModalUpdateBerita.vue";

import axios from 'axios'
export default {
  components: {
    ModalCreateBerita,
    ModalDetailBerita,
    ModalUpdateBerita
  },
  data: () => ({
    alertCreate: false,
    alertUpdate: false,
    modalDetail: false,
    modalEdit: false,
    selectedNews:{},
    search: '',
    headers: [
      { text: 'No', value: 'no' },
      { text: 'Judul Berita', value: 'judul' },
      { text: 'Kategori', value: 'kategori' },
      { text: 'Lokasi', value: 'lokasi' },
      { text: 'Waktu', value: 'timestamp' },
      { text: 'Isi Berita', value: 'isi' },
      { text: 'Action', value: 'action' }
    ],
    editedIndex: -1,
    editedItem: {
        judul: '',
        kategori: '',
        lokasi: '',
        waktu: '',
        isi: '',
    },
    defaultItem: {
        judul: '',
        kategori: '',
        lokasi: '',
        waktu: '',
        isi: '',
      }
    }),
    computed: {
      ...mapGetters({
          news:'getNews',
          categories:'getCategories'
      }),
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
      berita(){
        var berita = []
        var tempBerita
          for(var i = 0; i < this.news.length; i++){
            var tempKategori = ""
            var tempLokasi = ""
            var toLoopKategori = this.news[i].kategori
            var toLoopLokasi =  this.news[i].lokasi

            for(var j = 0; j < toLoopKategori.length; j++){
              if(toLoopKategori.length - j == 1){
                tempKategori += this.news[i].kategori[j]
              }else{
                tempKategori += this.news[i].kategori[j] + " - "
              }
            }

            for(var j = 0; j < toLoopLokasi.length; j++){
              if(toLoopLokasi.length - j == 1){
                tempLokasi += this.news[i].lokasi[j]
              }else{
                tempLokasi += this.news[i].lokasi[j] + ", "
              }
            }

            var tempDate = this.news[i].timestamp.split(' ')
            var date = tempDate[0]
            var tempClock = tempDate[1]
            var clock = tempClock.substring(0,5)

            tempBerita = {
              id: this.news[i].id,
              title: this.news[i].title,
              location: toLoopLokasi,
              idKategori: '',
              language:'id',
              kategori3: tempKategori,
              lokasi: tempLokasi,
              waktu: this.news[i].timestamp,
              jam: clock,
              date: date,
              isi: this.news[i].content,
              url: this.news[i].url,
              sitename: this.news[i].sitename,
              author: this.news[i].author 
            }
            berita.push(tempBerita)
          }
          return berita
      }
    },
    watch: {
      dialog (val) {
        val || this.close()
      }
    },
    methods: {
      closeDetail(event){
        this.modalDetail = event
      },
      closeEdit(event){
        this.modalEdit = event
      },
      popEdit (berita) {
        this.selectedNews = {
          id: berita.id,
          title: berita.title,
          location: berita.location,
          idKategori: '',
          language:'id',
          kategori3: berita.kategori3,
          lokasi: berita.lokasi,
          waktu: berita.waktu,
          jam: berita.jam,
          date: berita.date,
          isi: berita.isi,
          url: berita.url,
          sitename: berita.sitename,
          author: berita.author 
        }
        this.modalEdit = true
      },
      /*popDelete () {
        this.modalDelete = true
      },*/
      popDetail(berita){
        this.selectedNews = berita
        this.modalDetail = true
      },
      save () {
        if (this.editedIndex > -1) {
          Object.assign(this.news[this.editedIndex], this.editedItem)
        } else {
          this.news.push(this.editedItem)
        }
        this.close()
      },
      conciseNews(text){
        var result = text.substring(0,120) + "..."
        return result
      }
    },
    beforeMount() {
        this.$store.dispatch('getAllNews')
        this.$store.dispatch('getAllCategories')
    }
}
</script>
