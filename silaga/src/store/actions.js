// https://vuex.vuejs.org/en/actions.html
import axios from 'axios';


var defaultApi = 'http://127.0.0.1:5000/'

export default {
  getAllNews({commit}){
    axios({
      method: 'get',
      url: defaultApi + 'allnews'
      }).then(response => {
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
      })
  }
}
