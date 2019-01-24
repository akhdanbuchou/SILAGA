/**
 * Vuex
 *
 * @library
 *
 * https://vuex.vuejs.org/en/
 */

// Lib imports
import Vue from 'vue'
import Vuex from 'vuex'

// Store functionality
import actions from './actions'
import getters from './getters'
import modules from './modules'
import mutations from './mutations'


Vue.use(Vuex)

// Create a new store
const store = new Vuex.Store({
  state:{
    news: [],
    users: [],
    keyword: [],
    categories: []
  },
  actions,
  getters,
  modules,
  mutations,
})

export default store
