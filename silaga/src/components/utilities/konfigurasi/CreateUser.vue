<template>
    <div class="CreateUser">
        <v-dialog v-model="modalCreate" max-width="500px">
            <v-btn slot="activator" color="green darken-1 " dark class="mb-2 ml-3">Tambah Pengguna</v-btn>
            <v-card>
            <v-card-title>
                <span class="headline">Tambah Pengguna</span>
            </v-card-title>

            <v-card-text>
                <v-container grid-list-md>
                <v-layout wrap>
                    <v-flex xs6 sm6 md6>
                    <v-text-field v-model="newUser.nama" label="Nama"></v-text-field>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                        <v-select
                        :items="roles"
                        v-model="newUser.role"
                        label="Pilih Role"
                        ></v-select>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                    <v-text-field v-model="newUser.username" label="Username"></v-text-field>
                    </v-flex>
                    <v-flex xs6 sm6 md6>
                    <v-text-field type="password" v-model="newUser.password" label="Password"></v-text-field>
                    </v-flex>
                </v-layout>
                </v-container>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="close()">Cancel</v-btn>
                <v-btn color="blue darken-1" flat @click="createUser(newUser)">Save</v-btn>
            </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
export default {
    name:"CreateUser",
    data(){
        return{
            modalCreate: false,
            newUser:{
                nama:"",
                role:"",
                username:"",
                password:""
            },
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
        createUser (newUser) {
            console.log(newUser.nama)
            console.log(newUser.role)
            console.log(newUser.password)
            console.log(newUser.username)
            this.$store.dispatch('createUser', newUser)
            this.close()
        },
        close(){
            this.modalCreate = false
        }

    }
}
</script>

<style>

</style>
