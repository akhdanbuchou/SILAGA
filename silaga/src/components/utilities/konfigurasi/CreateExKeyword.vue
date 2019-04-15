<template>
    <div class="CreateExKeyword">
        <v-dialog v-model="modalCreateExKeyword" max-width="600px">
            <v-btn slot="activator" color="green darken-1 " dark class="mb-2 ml-3">Tambah Kata Kunci Pengecualian</v-btn>
            <v-card>
            <v-card-title>
                <span class="headline">Tambah Kata Kunci Pengecualian</span>
            </v-card-title>

            <v-card-text>
                <v-container grid-list-md>
                <v-layout wrap>
                    <v-flex xs12 sm12 md12>
                        <v-text-field v-model="newExKeyword" label="Kata Kunci Pengecualian"></v-text-field>
                    </v-flex>
                </v-layout>
                </v-container>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="close()">Cancel</v-btn>
                <v-btn color="blue darken-1" flat @click="createExKeyword(newExKeyword)">Save</v-btn>
            </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
export default {
    name:"CreateExKeyword",
    data(){
        return{
            modalCreateExKeyword: false,
            newExKeyword:''
        }
    },
    methods:{
        createExKeyword (newExKeyword) {
            this.$store.dispatch('createExKeyword', newExKeyword)
            this.close()
        },
        close(){
            this.modalCreateExKeyword = false
        }

    }
}
</script>

<style>

</style>
