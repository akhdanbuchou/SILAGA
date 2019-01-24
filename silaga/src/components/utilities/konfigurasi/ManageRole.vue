<template>
    <div class="ManageRole">
        <v-dialog v-model="modalCreate" max-width="700px">
            <v-btn slot="activator" color="green darken-3 " dark class="mb-2 ml-3">Pengaturan Role</v-btn> 
                <v-card>
                    <v-layout
                    justify-center
                    wrap
                    >
                        <v-flex md12>
                            <v-card-title>
                                <span class="headline">Atur Wewenang tiap Role</span>
                            </v-card-title>
                            <v-spacer></v-spacer>
                            <v-card-text>
                                <v-data-table
                                    :headers="headers"
                                    :items="roles"
                                    >
                                    <template slot="items" slot-scope="props">
                                    <td class="text-xs-left">{{ props.item.wewenang }}</td>
                                    <td>
                                        <v-checkbox
                                        v-model="props.item.user_config"
                                        value="1"
                                        primary
                                        hide-details
                                        ></v-checkbox>
                                    </td>
                                    <td>
                                        <v-checkbox
                                        v-model="props.item.berita_config"
                                        value="1"
                                        primary
                                        hide-details
                                        ></v-checkbox>
                                    </td>
                                    <td>
                                        <v-checkbox
                                        v-model="props.item.access_report"
                                        value="1"
                                        primary
                                        hide-details
                                        ></v-checkbox>
                                    </td>
                                    </template>
                                </v-data-table>
                            </v-card-text>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue darken-1" flat @click="close()">Cancel</v-btn>
                                <v-btn color="blue darken-1" flat @click="simpan(roles)">Save</v-btn>
                            </v-card-actions>
                        </v-flex>
                    </v-layout>
                </v-card>
        </v-dialog>
    </div>
</template>

<script>
export default {
    name:"ManageRole",
    props:['roles'],
    data(){
        return{
            headers:[
                {text:'Wewenang', value:'wewenang'},
                {text:'Konfigurasi User',value:'user_config'},
                {text:'Konfirugasi Berita',value:'berita_config'},
                {text:'Akses Laporan',value:'access_report'}
            ],
            modalCreate: false,
        }
    },
    methods:{
        close(){
            this.modalCreate = false
        },
        simpan(updated_roles){
            this.$store.dispatch('updateRoles', updated_roles)
            this.close()
        }

    }
}
</script>

<style>

</style>
