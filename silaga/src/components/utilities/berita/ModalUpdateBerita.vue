<template>
    <div class="ModalUpdateBerita">
        
        <v-card>
            <v-card-title>
                <span class="headline">Update Berita</span>
            </v-card-title>
            <v-card-text>
                <v-container grid-list-md>
                <v-layout wrap>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="selectedNews.title" label="Judul"></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-autocomplete
                        :loading="loading"
                        :items="objekKategori"
                        :search-input.sync="search"
                        v-model="selectedNews.kategori3"
                        cache-items
                        flat
                        hide-no-data
                        hide-details
                        label="Cari Kategori"
                        solo-inverted
                        ></v-autocomplete>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="selectedNews.lokasi" label="Lokasi"></v-text-field>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                        <v-menu
                            ref="menu"
                            :close-on-content-click="false"
                            v-model="menuJam"
                            :nudge-right="40"
                            :return-value.sync="selectedNews.jam"
                            lazy
                            transition="scale-transition"
                            offset-y
                            full-width
                            max-width="290px"
                            min-width="290px"
                        >   
                            <v-text-field
                            slot="activator"
                            v-model="selectedNews.jam"
                            label="Waktu Berita"
                            readonly
                            ></v-text-field>
                            <v-time-picker
                            v-if="menuJam"
                            v-model="selectedNews.jam"
                            full-width
                            @change="$refs.menu.save(selectedNews.jam)"
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
                            v-model="selectedNews.date"
                            label="Tanggal Berita"
                            readonly
                            ></v-text-field>
                            <v-date-picker v-model="selectedNews.date" @input="menuDate = false"></v-date-picker>
                        </v-menu>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                        <v-text-field v-model="selectedNews.author" label="Penulis"></v-text-field>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                        <v-text-field v-model="selectedNews.sitename" label="Nama Website"></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="selectedNews.url" label="Alamat URL"></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-textarea auto-grow box v-model="selectedNews.isi" label="Isi Berita"></v-textarea>
                    </v-flex>
                </v-layout>
                </v-container>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="close()">Batal</v-btn>
                <v-btn color="blue darken-1" flat @click="updateBerita(selectedNews)">Simpan</v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>
<script>
export default{
    name:"ModalUpdateBerita",
    data(){
        return{
            date: new Date().toISOString().substr(0, 10),
            menuJam: false,
            menuDate: false,
            loading: false,
            items: [],
            search: null,
            select: null
        }
    },
    props:['selectedNews','categories'],
    methods:{
        close () {
            this.$emit("closeEdit", false)
        },
        updateBerita(beritaToUpdate){
            var clock = beritaToUpdate.jam + ":00"
            beritaToUpdate.timestamp = beritaToUpdate.date + " " + clock
            this.$store.dispatch('updateBerita', beritaToUpdate)
            this.close()
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
        },
        kategoriSekarang(){
            var result = []
            for(var i = 0; i < this.categories.length; i++){
                if(this.categories[i].kategori.toLowerCase() == this.selectedNews.kategori){
                    console.log(this.categories[i].kategori)
                    var temp = {
                        value: this.categories[i].id,
                        text: this.categories[i].kategori,
                    }
                }
                result.push(temp)
            }
            return result
        }
    }

}
</script>