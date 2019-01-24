<template>
    <div class="ModalCreateBerita">
        <v-dialog v-model="modalCreate" max-width="500px">
            <v-btn slot="activator" color="green darken-1 " dark class="mb-2 ml-3">Tambah Berita</v-btn>
            <v-card>
                <v-card-title>
                    <span class="headline">Tambah Berita</span>
                </v-card-title>
                <v-card-text>
                    <v-container grid-list-md>
                    <v-layout wrap>
                        <v-flex xs12 sm12 md12>
                            <v-text-field v-model="newBerita.title" label="Judul"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm12 md12>
                            <v-autocomplete
                            :loading="loading"
                            :items="objekKategori"
                            :search-input.sync="search"
                            v-model="newBerita.kategori3"
                            cache-items
                            flat
                            hide-no-data
                            hide-details
                            label="Cari Kategori"
                            solo-inverted
                            ></v-autocomplete>
                        </v-flex>
                        <v-flex xs12 sm12 md12>
                            <v-text-field v-model="newBerita.lokasi" label="Lokasi"></v-text-field>
                        </v-flex>
                        <v-flex xs6 sm6 md6>
                            <v-menu
                                ref="menu"
                                :close-on-content-click="false"
                                v-model="menuJam"
                                :nudge-right="40"
                                :return-value.sync="jam"
                                lazy
                                transition="scale-transition"
                                offset-y
                                full-width
                                max-width="290px"
                                min-width="290px"
                            >   
                                <v-text-field
                                slot="activator"
                                v-model="jam"
                                label="Waktu Berita"
                                readonly
                                ></v-text-field>
                                <v-time-picker
                                v-if="menuJam"
                                v-model="jam"
                                full-width
                                @change="$refs.menu.save(jam)"
                                ></v-time-picker>
                            </v-menu>
                        </v-flex>
                        <v-flex xs6 sm6 md6>
                            <v-menu
                                :close-on-content-click="false"
                                v-model="menuDate"
                                :nudge-right="40"
                                lazy
                                transition="scale-transition"
                                offset-y
                                full-width
                                min-width="290px"
                            >
                                <v-text-field
                                slot="activator"
                                v-model="date"
                                label="Tanggal Berita"
                                readonly
                                ></v-text-field>
                                <v-date-picker v-model="date" @input="menuDate = false"></v-date-picker>
                            </v-menu>
                        </v-flex>
                        <v-flex xs6 sm6 md6>
                            <v-text-field v-model="newBerita.author" label="Penulis"></v-text-field>
                        </v-flex>
                        <v-flex xs6 sm6 md6>
                            <v-text-field v-model="newBerita.sitename" label="Nama Website"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm12 md12>
                            <v-text-field v-model="newBerita.url" label="Alamat URL"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm12 md12>
                            <v-textarea auto-grow box v-model="newBerita.isi" label="Isi Berita"></v-textarea>
                        </v-flex>
                    </v-layout>
                    </v-container>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" flat @click="close()">Cancel</v-btn>
                    <v-btn color="blue darken-1" flat @click="createBerita(newBerita)">Simpan</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>
<script>

export default {
    name:"ModalCreateBerita",
    props:['categories'],
    data(){
        return{
            date: new Date().toISOString().substr(0, 10),
            modalCreate: false,
            menuJam: false,
            menuDate: false,
            newBerita:{
                title: "",
                language: "id",
                kategori3: "",
                lokasi: "",
                timestamp:"",
                isi: "",
                url: "",
                sitename: "",
                author: ""
            },
            jam: "",
            date: "",
            loading: false,
            items: [],
            search: null,
            select: null
        }
    },
    computed:{
        objekKategori(){
            var result = []
            for(var i = 0; i < this.categories.length; i++){
                var temp = {
                    value: this.categories[i].id,
                    text: this.categories[i].kategori
                }
                result.push(temp)
            }
            return result
        }
    },
    methods:{
      popCreate (){
        this.modalCreate = true
      },
      close () {
        this.modalCreate = false,
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },
        createBerita(newBerita){
            var clock = this.jam + ":00"
            newBerita.timestamp = this.date + " " + clock
            this.$store.dispatch('createBerita', newBerita)
            this.close()
      }
    }

}


</script>
