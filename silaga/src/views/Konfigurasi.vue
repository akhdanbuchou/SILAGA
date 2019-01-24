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
            Daftar Pengguna
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
            <v-icon>mdi-magnify</v-icon>

          <CreateUser></CreateUser>
          <v-dialog v-model="modalEdit" max-width="500px">
            <UpdateUser :selectedPengguna="selectedPengguna" v-on:closeUpdate="closeUpdate($event)"></UpdateUser>
          </v-dialog>
          <ManageRole :roles="roles"></ManageRole>
            
          </v-card-title>
          <v-progress-circular v-if="users.length == 0" class="mb-3 ml-3"
            row wrap align-center justify-center
            :width="3"
            color="green"
            indeterminate
          ></v-progress-circular>
          <v-data-table v-else
            :headers="headers"
            :items="users"
            :search="search"
          >
            <template slot="items" slot-scope="props">
              <td>{{ props.item.id }}</td>
              <td class="text-xs-left">{{ props.item.nama }}</td>
              <td class="text-xs-left">{{ props.item.wewenang }}</td>
              <td class="text-xs-left">{{ props.item.username }}</td>
              <td class="justify-left pl-3 layout px-0">
                <v-icon
                  small
                  class="mr-2"
                  @click="popUpdate(props.item)"
                >
                  mdi-pencil
                </v-icon>
                <v-icon
                  small
                  class="mr-2"
                  @click="popDelete(props.item)"
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
import axios from 'axios';
import CreateUser from "@/components/utilities/user/CreateUser.vue";
import UpdateUser from "@/components/utilities/user/UpdateUser.vue";
import ManageRole from "@/components/utilities/user/ManageRole.vue";

export default {
  components:{
      CreateUser,
      UpdateUser,
      ManageRole
  },
  data: () => ({
    search: '',
    selectedPengguna:{},
    modalEdit: false,
    headers: [
      { text: 'No', value: 'id'},
      { text: 'Nama', value: 'nama' },
      { text: 'Role', value: 'role' },
      { text: 'Username', value: 'username' },
      { text: 'Action', value: 'action' }
    ],
    urutan:1,
    editedIndex: -1,
    defaultItem: {
        nama: '',
        role: '',
        username: '',
        password: ''
      }
    }),
    computed: {
      ...mapGetters({
          users:'getUsers',
          roles:'getRoles'
      }),
      formTitle () {
        return 'Buat Pengguna Baru'
      },
      pengguna(){
        var pengguna = []
        var tempPengguna
        for(var i = 0; i < this.users.length; i++){
            tempPengguna = {
              id: this.users[i].id,
              nama: this.users[i].nama,
              role: this.users[i].role,
              username: this.users[i].username
            }
            pengguna.push(tempPengguna)
          }
        return pengguna
      }
    },
    watch: {
      dialog (val) {
        val || this.close()
      }
    },
    methods: {
      popUpdate(pengguna){
        this.selectedPengguna = {
          id: pengguna.id,
          nama: pengguna.nama,
          username: pengguna.username,
          peran:{
            value: pengguna.role,
            text: pengguna.wewenang
          }
        }
        this.modalEdit = true
      },
      closeUpdate(event){
        this.modalEdit = event
      }
    },
    beforeMount(){
      this.$store.dispatch('getAllUsers')
      this.$store.dispatch('getAllRoles')
    }
}
</script>
