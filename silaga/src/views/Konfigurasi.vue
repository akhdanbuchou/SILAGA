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
              v-model="searchUser"
              label="Cari Pengguna"
            ></v-text-field>
            <v-icon>mdi-magnify</v-icon>

          <CreateUser></CreateUser>

          <v-dialog v-model="modalEdit" max-width="500px">
            <UpdateUser :selectedPengguna="selectedPengguna" v-on:closeUpdate="closeUpdate($event)"></UpdateUser>
          </v-dialog>

          <ManageRole :roles="roles"></ManageRole>

          <v-dialog v-model="modalCategory" max-width="500px">
            <CategoryDetail :selectedCategory="selectedCategory" v-on:closeCategory="closeCategory($event)"></CategoryDetail>
          </v-dialog>

          <v-dialog v-model="modalDeletePengguna" max-width="500px">
              <v-card>
                  <v-card-title>
                      <span>Apa anda yakin ingin menghapus pengguna dengan username: </span>
                      <br>
                      <span class="title font-weight-black"> {{toDeletePengguna.username}} ? </span>
                  </v-card-title>

                  <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn class="font-weight-bold" color="blue darken-1" flat @click="closeDelete()">Batal</v-btn>
                      <v-btn class="font-weight-bold" color="red darken-1" flat @click="deletePengguna()">Hapus</v-btn>
                  </v-card-actions>
              </v-card>
          </v-dialog>

          <v-dialog v-model="modalDeleteExKeyword" max-width="500px">
              <v-card>
                  <v-card-title>
                      <span>Apa anda yakin ingin menghapus keyword pengecualian: </span>
                      <br>
                      <span class="title font-weight-black"> {{toDeleteExKeyword.keyword}} ? </span>
                  </v-card-title>

                  <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn class="font-weight-bold" color="blue darken-1" flat @click="closeDelete()">Batal</v-btn>
                      <v-btn class="font-weight-bold" color="red darken-1" flat @click="deleteExKeyword()">Hapus</v-btn>
                  </v-card-actions>
              </v-card>
          </v-dialog>
            
          </v-card-title>
          <v-progress-circular v-if="users.length == 0" class="mb-3 ml-3"
            row wrap align-center justify-center
            :width="3"
            color="green"
            indeterminate
          ></v-progress-circular>
          <v-data-table v-else
            :headers="userHeaders"
            :items="userTable(pengguna, searchUser)"
          >
            <template slot="items" slot-scope="props">
                <td>{{props.index + 1}}</td>
                <td class="text-xs-left">{{ props.item.nama }}</td>
                <td class="text-xs-left">{{ props.item.wewenang }}</td>
                <td class="text-xs-left">{{ props.item.username }}</td>
                <td class="justify-left pl-3 layout px-0">
                  <v-icon
                    small
                    class="mr-2"
                    @click="popUpdateUser(props.item)"
                    color="green"
                  >
                    mdi-pencil
                  </v-icon>
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
              Your search for "{{ searchUser }}" found no results.
            </v-alert>
          </v-data-table>
        </v-card>

        <v-card class="mt-4">
          <v-card-title class="font-weight-medium">
            Daftar Golongan Gangguan dan Kata Kunci
            <v-spacer></v-spacer>
            <v-text-field
              v-model="searchKeyword"
              label="Cari Kategori"
            ></v-text-field>
            <v-icon>mdi-magnify</v-icon>
            
          </v-card-title>
          <v-progress-circular v-if="keywords.length == 0" class="mb-3 ml-3"
            row wrap align-center justify-center
            :width="3"
            color="green"
            indeterminate
          ></v-progress-circular>
          <v-data-table v-else
            :headers="keywordHeaders"
            :items="keywordTable(keywords, searchKeyword)"
          >
            <template slot="items" slot-scope="props">
              <td>{{ props.item.idKategori }}</td>
              <td class="text-xs-left">{{ props.item.gol }}</td>
              <td class="text-xs-left">{{ props.item.sgol }}</td>
              <td class="text-xs-left">{{ props.item.ssgol }}</td>
              <td class="text-xs-left">{{ countKey(props.item.keyword) }}</td>
              <td class="justify-left pl-3 layout px-0">
                <v-icon
                  small
                  class="mr-2"
                  @click="popUpdateCategory(props.item)"
                  color="green"
                >
                  mdi-pencil
                </v-icon>
              </td>
            </template>
            <v-alert slot="no-results" :value="true" color="error" icon="mdi-warning">
              Your search for "{{ searchKeyword }}" found no results.
            </v-alert>
          </v-data-table>
        </v-card>

        <v-card class="mt-4">
          <v-card-title class="font-weight-medium">
            Daftar Kata Kunci Pengecualian
            <v-spacer></v-spacer>
            <v-text-field
              v-model="searchExKeyword"
              label="Cari Kata Kunci"
            ></v-text-field>
            <v-icon>mdi-magnify</v-icon>
            <CreateExKeyword></CreateExKeyword>
          </v-card-title>
          <v-progress-circular v-if="keywords.length == 0" class="mb-3 ml-3"
            row wrap align-center justify-center
            :width="3"
            color="green"
            indeterminate
          ></v-progress-circular>
          <v-data-table v-else
            :headers="exKeywordHeaders"
            :items="exKeywordTable(exKeywords, searchExKeyword)"
          >
            <template slot="items" slot-scope="props">
              <td>{{ props.index + 1 }}</td>
              <td class="text-xs-left">{{ props.item.keyword }}</td>
              <td class="justify-left pl-3 layout px-0">
                <v-icon
                  small
                  class="mr-2"
                  @click="popDeleteEx(props.item)"
                  color="red"
                  >
                  mdi-delete
                </v-icon>
              </td>
            </template>
            <v-alert slot="no-results" :value="true" color="error" icon="mdi-warning">
              Your search for "{{ searchKeyword }}" found no results.
            </v-alert>
          </v-data-table>
        </v-card>
      </v-flex>
    </v-layout>

  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import CreateUser from "@/components/utilities/konfigurasi/CreateUser.vue"
import CreateExKeyword from "@/components/utilities/konfigurasi/CreateExKeyword.vue"
import UpdateUser from "@/components/utilities/konfigurasi/UpdateUser.vue"
import ManageRole from "@/components/utilities/konfigurasi/ManageRole.vue"
import CategoryDetail from "@/components/utilities/konfigurasi/CategoryDetail.vue"

export default {
  components:{
      CreateUser,
      UpdateUser,
      ManageRole,
      CategoryDetail,
      CreateExKeyword
  },
  data: () => ({
    searchUser: '',
    searchExKeyword:'',
    searchKeyword:'',
    selectedPengguna:{},
    selectedCategory:{},
    toDeletePengguna:{},
    toDeleteExKeyword:{},
    modalDeletePengguna: false,
    modalDeleteExKeyword: false,
    modalEdit: false,
    modalCategory: false,
    userHeaders: [
      { text: 'No', value: 'no'},
      { text: 'Nama', value: 'nama' },
      { text: 'Role', value: 'role' },
      { text: 'Username', value: 'username' },
      { text: 'Action', value: 'action' }
    ],
    keywordHeaders: [
      { text: 'No', value: 'no'},
      { text: 'Golongan Utama', value: 'nama1' },
      { text: 'Sub-Golongan', value: 'nama2' },
      { text: 'Sub-Sub-Golongan', value: 'nama3' },
      { text: 'Jumlah Kata Kunci', value: 'keyCount' },
      { text: 'Action', value: 'action' }
    ],
    exKeywordHeaders: [
      { text: 'No', value: 'no'},
      { text: 'Kata Kunci', value: 'keyword' },
      { text: 'Action', value: 'action' },
    ],
    urutan:1,
    }),
    computed: {
      ...mapGetters({
          users:'getUsers',
          roles:'getRoles',
          tempKeywordTable:'getKeywordTable',
          tempExKeywordTable:'getExKeywordTable'
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
              wewenang: this.users[i].wewenang,
              username: this.users[i].username
            }
            pengguna.push(tempPengguna)
          }
        return pengguna
      },
      keywords(){
        var result= []
        for(var i = 0; i < this.tempKeywordTable.length; i++){
          var spliter = this.tempKeywordTable[i].namaKategori3.split(" - ")
          var gol = spliter[0]
          var sgol = spliter[1]
          var ssgol = spliter[2]
          var temp = {
            idKategori: this.tempKeywordTable[i].idKategori3,
            gol: gol,
            sgol: sgol,
            ssgol: ssgol,
            keyword: this.tempKeywordTable[i].keyword
          }
          result.push(temp)
        }
        return result
      },
      exKeywords(){
        var result= []
        for(var i = 0; i < this.tempExKeywordTable.length; i++){
          var temp = {
            id: this.tempExKeywordTable[i].id,
            keyword: this.tempExKeywordTable[i].keyword
          }
          result.push(temp)
        }
        return result
      }
    },
    watch: {
      dialog (val) {
        val || this.close()
      }
    },
    methods: {
      userTable(list, keyword){
        var keyUpper = keyword.charAt(0).toUpperCase() + keyword.slice(1);
        if(keyword != null){
          return list.filter(element => {
            return element.nama.indexOf(keyword) > -1 || 
                  element.nama.indexOf(keyUpper) > -1 ||
                  element.wewenang.indexOf(keyUpper) > -1 ||
                  element.username.indexOf(keyword) > -1 
          });
        }else {
          return list
        }
      },
      keywordTable(list, keyword){
        var keyUpper = keyword.charAt(0).toUpperCase() + keyword.slice(1);
        if(keyword != null){
          return list.filter(element => {
            return element.gol.indexOf(keyUpper) > -1 ||
                  element.sgol.indexOf(keyUpper) > -1 ||
                  element.ssgol.indexOf(keyUpper) > -1
          });
        }else {
          return list
        }
      },
      exKeywordTable(list, keyword){
        if(keyword != null){
          return list.filter(element => {
            return element.keyword.indexOf(keyword) > -1
          });
        }else {
          return list
        }
      },
      popUpdateUser(pengguna){
        this.selectedPengguna = {
          id: pengguna.id,
          nama: pengguna.nama,
          username: pengguna.username,
          peran: pengguna.role
        }
        this.modalEdit = true
      },
      popUpdateCategory(category){
        this.selectedCategory = {
          idKategori: category.idKategori,
          nama: category.gol + " - " + category.sgol + " - " + category.ssgol,
          objKeyword: category.keyword,
        }
        this.modalCategory = true
      },
      popDelete(pengguna){
        this.modalDeletePengguna = true
        this.toDeletePengguna = pengguna
      },
      popDeleteEx(exKeyword){
        this.modalDeleteExKeyword = true
        this.toDeleteExKeyword = exKeyword
      },
      deletePengguna(){
        this.$store.dispatch('deleteUser', this.toDeletePengguna)
        this.closeDelete()
      },
      deleteExKeyword(){
        this.$store.dispatch('deleteExKeyword', this.toDeleteExKeyword)
        this.closeDelete()
      },
      closeDelete(){
        this.modalDeletePengguna = false
        this.modalDeleteExKeyword = false
      },
      closeUpdate(event){
        this.modalEdit = event
      },
      closeCategory(event){
        this.modalCategory = event
      },
      countKey(keywords){
        return keywords.length
      }
    },
    beforeMount(){
      this.$store.dispatch('getAllUsers')
      this.$store.dispatch('getAllRoles')
      this.$store.dispatch('getKeywordTable')
      this.$store.dispatch('getExKeywordTable')
    }
}
</script>
