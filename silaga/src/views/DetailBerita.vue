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

            <v-dialog max-width="500px">
              <v-btn slot="activator" color="green darken-1 " dark class="mb-2 ml-3">Tambah Laporan</v-btn>
              <v-card>
                <v-card-title>
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container grid-list-md>
                    <v-layout wrap>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.id" label="No Berita"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.judul" label="Judul"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.kategori" label="Kategori"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.lokasi" label="Lokasi"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.timestamp" label="Waktu"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.isi" label="Konten"></v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
                  <v-btn color="blue darken-1" flat @click="save">Save</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="berita"
            :search="search"
          >
            <template slot="items" slot-scope="props">
              <td class="text-xs-left">{{ props.item.judul }}</td>
              <td class="text-xs-left">{{ props.item.kategori }}</td>
              <td class="text-xs-left">{{ props.item.lokasi }}</td>
              <td class="text-xs-left">{{ props.item.waktu }}</td>
              <td class="text-xs-left">{{ props.item.isi }}</td>
              <td class="justify-left pl-3 layout px-0">
                <v-icon
                  small
                  class="mr-2"
                  @click="editItem(props.item)"
                >
                  mdi-pencil
                </v-icon>
                <v-icon
                  small
                  @click="deleteItem(props.item)"
                >
                  mdi-delete
                </v-icon>
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

import axios from 'axios'
export default {
  data: () => ({
    search: '',
    headers: [
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
          news:'getNews'
      }),
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
      berita(){
        var berita = []
        var tempBerita
          for(var i = 0; i < this.news.length; i++){
            tempBerita = {
              judul: this.news[i].judul,
              kategori: this.news[i].kategori,
              lokasi: this.news[i].lokasi,
              waktu: this.news[i].timestamp,
              isi: this.news[i].isi
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
      editItem (item) {
        this.editedIndex = this.news.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
      deleteItem (item) {
        const index = this.news.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.news.splice(index, 1)
      },
      close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },
      save () {
        if (this.editedIndex > -1) {
          Object.assign(this.news[this.editedIndex], this.editedItem)
        } else {
          this.news.push(this.editedItem)
        }
        this.close()
      }
    },
    beforeMount() {
        this.$store.dispatch('getAllNews')
    }
}
</script>
