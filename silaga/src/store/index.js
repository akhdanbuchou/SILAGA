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
    //dashboard
    frekuensiRekap:'',
    loadPopTableFlag: false,
    flagLayer1:false,
    filterLayer1: '',
    dateFilter:[],
    popTable:[],
    csvHeader:[],
    csvData:[],
    excelHeader:{},
    excelData: [],
    lineData: [],
    lineChart: {},
    lineToPrint:{},
    pieData: [],
    pieChart: {},
    pieToPrint:[],

    //Detail Berita
    news: [],

    //Laporan Lapangan
    telegram: [],
    media:[],
    mediaGambar:[],
    mediaVideo:[],

    //Konfigurasi Sistem
    users: [],
    keywordTable:[],
    keyword: [],
    categories: [],
    gangguanGol1:[],
    currentRole:{},
    roles:[]
  },
  actions,
  getters,
  modules,
  mutations,
})

export default store
