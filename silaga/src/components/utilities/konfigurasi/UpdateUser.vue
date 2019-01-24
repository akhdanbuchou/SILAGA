<template>
    <div class="UpdateUser">
        <v-card>
            <v-card-title>
                <span class="headline">Tambah Pengguna</span>
            </v-card-title>

            <v-card-text>
                <v-container grid-list-md>
                <v-layout wrap>
                    <v-flex xs6 sm6 md6>
                    <v-text-field v-model="selectedPengguna.nama" label="Nama"></v-text-field>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                        <v-select
                        :items="roles"
                        menu-props="auto"
                        v-model="selectedPengguna.peran"
                        label="Pilih Role"
                        ></v-select>
                    </v-flex>
                    <v-flex xs12 sm12 md12>
                    <v-text-field v-model="selectedPengguna.username" label="Username"></v-text-field>
                    </v-flex>
                </v-layout>
                </v-container>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="close()">Cancel</v-btn>
                <v-btn color="blue darken-1" flat @click="updateUser(selectedPengguna)">Save</v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>
export default {
    name:"UpdateUser",
    props:['selectedPengguna','modalEdit'],
    data(){
        return{
            roles:
            [
                {text:"Bintang",value:90},
                {text:"Melati Menengah",value:91},
                {text:"Melati Pertama",value:92},
                {text:"Personal",value:93},
                {text:"Pemda DKI",value:94}
            ]     
        }
    },
    methods:{
        updateUser (newUser) {
            this.$store.dispatch('updateUser', newUser)
            this.close()
        },
        close(){
            this.$emit("closeUpdate", false)
        }

    }
}
</script>

<style>

</style>
