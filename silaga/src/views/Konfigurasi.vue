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

            <v-dialog v-model="modalCreate" max-width="500px">
              <v-btn slot="activator" color="green darken-1 " dark class="mb-2 ml-3">Tambah Pengguna</v-btn>
              <v-card>
                <v-card-title>
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container grid-list-md>
                    <v-layout wrap>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.nama" label="Nama"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.role" label="Role"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.username" label="Username"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field type="password" v-model="editedItem.password" label="Password"></v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
                  <v-btn color="blue darken-1" flat @click="createUser(editedItem)">Save</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="pengguna"
            :search="search"
          >
            <template slot="items" slot-scope="props">
              <td>{{ props.item.id }}</td>
              <td class="text-xs-left">{{ props.item.nama }}</td>
              <td class="text-xs-left">{{ props.item.role }}</td>
              <td class="text-xs-left">{{ props.item.username }}</td>
              <td class="justify-left pl-3 layout px-0">
                <v-icon
                  small
                  class="mr-2"
                  @click="deleteUser(props.item)"
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

export default {
  data: () => ({
    modalCreate: false,
    search: '',
    headers: [
      { text: 'No', value: 'id'},
      { text: 'Nama', value: 'nama' },
      { text: 'Role', value: 'role' },
      { text: 'Username', value: 'username' },
      { text: 'Action', value: 'action' }
    ],
    urutan:1,
    editedIndex: -1,
    editedItem: {
        nama: '',
        role: '',
        username: '',
        password: ''
    },
    defaultItem: {
        nama: '',
        role: '',
        username: '',
        password: ''
      }
    }),
    computed: {
      ...mapGetters({
          users:'getUsers'
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
      deleteUser (item) {
        console.log(item)
      },
      createUser (newUser) {
        this.$store.dispatch('createUser', newUser)
        this.close()
      }
    },
    beforeMount(){
      this.$store.dispatch('getAllUsers')
    }
}
</script>
