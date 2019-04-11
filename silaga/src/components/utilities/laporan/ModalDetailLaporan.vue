<template>
    <div class="ModalDetailLaporan">
        <v-card>
            <v-card-title>
                <span class="headline">Detail Berita</span>
            </v-card-title>
            <v-card-text>
                <v-container grid-list-md>
                <v-layout wrap>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="selectedLaporan.pelapor" label="Pelapor" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="selectedLaporan.kategori" label="Kategori" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="selectedLaporan.timestamp" label="Waktu Laporan Diterima" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-textarea auto-grow box v-model="selectedLaporan.isi" label="Isi Laporan" readonly></v-textarea>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-btn color="green darken-2" dark @click="muatMedia()">
                            Muat Media
                        </v-btn>
                    </v-flex>
                    
                    <div v-if="mediaFlag && media.length == 0">
                        <v-flex  xs12 sm12 md12>
                            Media Tidak Ditemukan...
                        </v-flex>
                    </div>
                    <div v-else>
                        <v-flex v-if="mediaGambar.length != 0" 
                        xs12 sm12 md12 v-for="gambar in mediaGambar" :key="gambar">
                            <img style="width: 100%;height: 100%" :src="'data:image/jpg;base64, ' + muatGambar64(gambar)" alt="Harap Tunggu..." />
                        </v-flex>
                        <v-flex v-if="mediaVideo.length != 0" 
                        xs12 sm12 md12 v-for="video in mediaVideo" :key="video">
                            <video width="100%" controls>
                                <source type="video/mp4" :src="'data:video/mp4;base64, ' + muatVideo64(video)" >
                            </video>
                        </v-flex>
                    </div>
                </v-layout>
                </v-container>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="close()">OK</v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
import axios from 'axios'
const defaultApi = "http://5.79.64.131:18880/"

export default{
    name:"ModalDetailLaporan",
    data(){
        return{
            mediaFlag: false,
            base64:'',
            gambar:'',
            video:''
        }
    },
    props:['selectedLaporan'],
    methods:{
        muatGambar64(gambar){
            axios({
                method: 'get',
                url: defaultApi + 'getfile/' + gambar
            }).then(response => {
                this.gambar = response.data
            })
            return this.gambar
        },
        muatVideo64(video){
            console.log(video)
            axios({
                method: 'get',
                url: defaultApi + 'getfile/' + video
            }).then(response => {
                this.video = response.data
            })
            return this.video
        },
        muatMedia(){
            axios({
                method: 'get',
                url: defaultApi + 'nontext/' + this.selectedLaporan.id
            }).then(response => {
                this.$store.commit('setMedia', response.data)
                this.mediaFlag = true
            })

            
        },
        close () {
            this.$emit("closeDetail", false)
            this.$store.commit('emptyMedia')
            this.mediaFlag = false
            this.gambar = ''
            this.video = ''
        }
    },
    computed:{
        ...mapGetters({
          mediaGambar:'getMediaGambar',
          mediaVideo:'getMediaVideo',
          media:'getMedia'
        })
        
        
    }

}
</script>