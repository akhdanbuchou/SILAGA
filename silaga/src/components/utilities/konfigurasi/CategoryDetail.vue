<template>
    <div class="CategoryDetail">
        <v-card class="px-3">
            <v-card-title>
                <span class="headline">Atur Kata Kunci Gangguan:</span>
                <span class="headline">{{selectedCategory.nama}}</span>
            </v-card-title>
            <v-spacer></v-spacer>

            <v-dialog v-model="modalCreate" max-width="500px">
                <v-btn slot="activator" color="green darken-1 " dark class="mb-2 ml-3">Tambah Kata Kunci</v-btn>
                <v-card>
                <v-card-title>
                    <span class="headline">Tambah Kata Kunci untuk gangguan: </span>
                    <span class="headline">{{selectedCategory.nama}} </span>
                </v-card-title>

                <v-card-text>
                    <v-container grid-list-md>
                    <v-layout wrap>
                        <v-flex xs12 sm12 md12>
                         <v-text-field v-model="newKey" label="Nama Keyword"></v-text-field>
                        </v-flex>
                    </v-layout>
                    </v-container>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn class="font-weight-bold" color="blue darken-1" flat @click="closeCreate()">Cancel</v-btn>
                    <v-btn class="font-weight-bold" color="blue darken-1" flat @click="createKeyword()">Save</v-btn>
                </v-card-actions>
                </v-card>
            </v-dialog>

            <v-dialog v-model="modalDelete" max-width="500px">
                <v-card>
                    <v-card-title>
                        <span class="title">Apa anda yakin ingin menghapus kata kunci 
                            <span class="title font-weight-black"> {{keyToDelete}} ? </span>
                        </span>
                    </v-card-title>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn class="font-weight-bold" color="blue darken-1" flat @click="closeDelete()">Batal</v-btn>
                        <v-btn class="font-weight-bold" color="red darken-1" flat @click="deleteKeyword()">Hapus</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

            <v-data-table
                :headers="headers"
                :items="keywords"
                :search="search"
            >
                <template slot="items" slot-scope="props">
                <td>{{ props.index + 1 }}</td>
                <td class="text-xs-left">{{ props.item.namaKeyword }}</td>
                <td class="justify-left pl-3 layout px-0">
                    <v-icon
                    small
                    class="mr-2"
                    @click="popDelete(props.item)"
                    color="red"
                    >
                    mdi-delete
                    </v-icon>
                </td>
                </template>
                <v-alert slot="no-results" :value="true" color="error" icon="mdi-warning">
                Your search for "{{ search }}" found no results.
                </v-alert>
            </v-data-table>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="closeDetail()">Selesai</v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>
export default {
    name:"CategoryDetail",
    props:['modalCategory','selectedCategory'],
    data(){
        return{
            search:'',
            headers:[
                {text:'No',value:'no'},
                {text:'Keyword',value:'keyword'},
                {text:'Action',value:'action'}
            ],
            modalDelete:false,
            modalCreate:false,
            newKey:'',
            idToDelete:'',
            keyToDelete:''
        }
    },
    computed:{
        keywords(){
            return this.selectedCategory.objKeyword
        }
    },
    methods:{
        closeDetail(){
            this.$emit("closeCategory", false)
        },
        closeCreate(){
            this.modalCreate = false
        },
        closeDelete(){
            this.modalDelete = false
        },
        popDelete(newKey){
            this.idToDelete = newKey.idKeyword
            this.keyToDelete = " " + newKey.namaKeyword
            this.modalDelete = true
        },
        createKeyword(){
            var keyBaru = this.newKey
            var newKeyword = {
                keyword: keyBaru,
                kategori3: this.selectedCategory.idKategori
            }
            this.$store.dispatch("createKeyword", newKeyword)
            this.$emit("updateKeyword")
            this.closeCreate()
        },
        deleteKeyword(){
            this.$store.dispatch("deleteKeyword", this.idToDelete)
            this.$emit("updateKeyword")
            this.closeDelete()
        }
    }
}
</script>

<style>

</style>
