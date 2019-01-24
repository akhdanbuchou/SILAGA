// https://vuex.vuejs.org/en/actions.html
import axios from 'axios';


var defaultApi = 'http://127.0.0.1:5000/'

export default {
  getAllNews({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'allnews'
      }).then(response => {
          //console.log(response.data[0])
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
  getAllCategories({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'categories3',
    }).then(response => {
        commit('setCategories', response.data)
    })
  },
  createUpdateBerita({commit}, newBerita){
    axios({
      method: 'post',
      url: defaultApi + 'createUpdateBerita',
      data:{
        title: newBerita.title,
        language: newBerita.language,
        kategori3: newBerita.kategori3,
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
        }).then(response => {
            commit('setAllNews', response.data)
        })
    })
  }
  
}
