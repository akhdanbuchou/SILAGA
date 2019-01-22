<template>
    <div class="ModalDetailBerita">
        <v-card>
            <v-card-title>
                <span class="headline">Detail Berita</span>
            </v-card-title>
            <v-card-text>
                <v-container grid-list-md>
                <v-layout wrap>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="selectedNews.judul" label="Judul" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                        <v-text-field v-model="selectedNews.kategori" label="Kategori" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                        <v-text-field v-model="selectedNews.lokasi" label="Lokasi" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                        <v-text-field v-model="selectedNews.waktu" label="Waktu" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                        <v-text-field v-model="selectedNews.author" label="Penulis" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="selectedNews.sitename" label="Nama Website" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="selectedNews.url" label="Alamat URL" readonly></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                        <v-textarea auto-grow box v-model="selectedNews.isi" label="Isi Berita" readonly></v-textarea>
                    </v-flex>
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
export default{
    name:"ModalDetailBerita",
    data(){
        return{

        }
    },
    props:['selectedNews'],
    methods:{
        close () {
            this.$emit("closeDetail", false)
        },
    }

}
</script>