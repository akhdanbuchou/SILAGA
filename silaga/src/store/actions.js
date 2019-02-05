// https://vuex.vuejs.org/en/actions.html
import axios from 'axios';


var defaultApi = "http://5.79.64.131:18880/"

export default {
  getAllNews({commit}, jumlah){
    axios.get(defaultApi + 'allnews/' + jumlah)
    .then(response => {
          commit('setAllNews', response.data)
      })
  },
  getAllUsers({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'users'
      }).then(response => {
          commit('setAllUsers', response.data)
      })
  },
  createUser({commit}, newUser){
    axios({
      method: 'post',
      url: defaultApi + 'createUser',
      data:{
        username: newUser.username,
        password: newUser.password,
        nama: newUser.nama,
        role: newUser.role
      }
      }).then(response => {
        axios({
          method: 'get',
          url: defaultApi + 'users'
          }).then(res => {
              commit('setAllUsers', res.data)
          })
      })
  },
  updateUser({commit}, newUser){
    axios({
      method: 'post',
      url: defaultApi + 'updateUser',
      data:{
        id: newUser.id,
        username: newUser.username,
        nama: newUser.nama,
        role: newUser.role
      }
      }).then(response => {
        axios({
          method: 'get',
          url: defaultApi + 'users'
          }).then(res => {
              commit('setAllUsers', res.data)
          })
      })
  },
  deleteUser({commit}, oldUser){
    axios({
      method: 'post',
      url: defaultApi + 'deleteUser',
      data:{
        idUser: oldUser.id,
      }
      }).then(response => {
        axios({
          method: 'get',
          url: defaultApi + 'users'
          }).then(res => {
              commit('setAllUsers', res.data)
          })
      })
  },
  getFirstCategories({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'categories',
    }).then(response => {
        commit('setGangguanGol1', response.data)
    })
  },
  getAllCategories({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'categories3',
    }).then(response => {
        commit('setCategories', response.data)
    })
  },
  createBerita({commit}, newBerita){
    axios({
      method: 'post',
      url: defaultApi + 'createBerita',
      data:{
        title: newBerita.title,
        language: newBerita.language,
        kategori: newBerita.kategori3,
        lokasi: newBerita.lokasi,
        timestamp: newBerita.timestamp,
        content: newBerita.isi,
        url: newBerita.url,
        sitename: newBerita.sitename,
        author: newBerita.author
      }
    }).then(response => {
      axios({
        method: 'get',
        url: defaultApi + 'allnews'
        }).then(res => {
            commit('setAllNews', res.data)
        })
    })
  },
  updateBerita({commit}, newBerita){
    axios({
      method: 'post',
      url: defaultApi + 'updateBerita',
      data:{
        id: newBerita.id,
        title: newBerita.title,
        language: newBerita.language,
        kategori: newBerita.kategori3,
        lokasi: newBerita.lokasi,
        timestamp: newBerita.timestamp,
        content: newBerita.isi,
        url: newBerita.url,
        sitename: newBerita.sitename,
        author: newBerita.author
      }
    }).then(response => {
      axios({
        method: 'get',
        url: defaultApi + 'allnews'
        }).then(res => {
            commit('setAllNews', res.data)
        })
    })
  },
  getAllRoles({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'roles',
    }).then(response=>{
      commit('setRoles', response.data)
    })
  },
  getCurrentRole({commit}, roleId){
    axios.get(defaultApi + 'role?id=' + roleId)
      .then(response => {
        console.log(response.data)
        commit('setCurrentRole', response.data)
      })
  },
  updateRoles({commit}, updated_roles){
    axios({
      method: 'post',
      url: defaultApi + 'updateRole',
      data:{
        updated_roles: updated_roles
      }
    }).then(response => {
      axios({
        method: 'get',
        url: defaultApi + 'roles',
      }).then(response=>{
        commit('setRoles', response.data)
      })
    })
  },
  getTelegramReport({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'allreports'
    }).then(response => {
      commit('setTelegramReport', response.data)
    })
  },
  getKeywordTable({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'keywords'
    }).then(response => {
      commit('setKeywordTable', response.data)
    })
  },
  createKeyword({commit}, objKeyword){
    axios({
      method: 'post',
      url: defaultApi + 'createKeyword',
      data:{
        keyword: objKeyword.keyword,
        kategori3: objKeyword.kategori3
      }
    }).then(response => {
      
    })
  },
  deleteKeyword({commit}, idKey){
    axios({
      method: 'post',
      url: defaultApi + 'deleteKeyword',
      data:{
        idKeyword: idKey
      }
    }).then(response => {
      
    })
  },
  getDefaultLineChart({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'rekap/0/-/-/-/bulanan'
    }).then(response => {
      commit('setLineChart',response.data)
    })

  },
  getDefaultPieChart({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'pie-chart/0/-/-/-'
    }).then(response => {
      response.data.selectedGangguan = '0'
      commit('setPieChart',response.data)
    })
  }
  
}
