// https://vuex.vuejs.org/en/getters.html

export default {
  getNews(state){
    return state.news
  },
  getUsers(state){
    return state.users
  },
  getKeywords(state){
    return state.keywords
  },
  getCategories(state){
    return state.categories
  },
  getRoles(state){
    return state.roles
  },
  getCurrentRole(state){
    return state.currentRole
  },
  getTelegramReport(state){
    return state.telegram
  },
  getKeywordTable(state){
    return state.keywordTable
  },
  getLineData(state){
    return state.lineData
  },
  getGangguanGol1(state){
    return state.gangguanGol1
  },
  getLineChart(state){
    return state.lineChart
  },
  getPieData(state){
    return state.pieData
  },
  getPieChart(state){
    return state.pieChart
  },
  getMap(state){
    return state.map
  },
  getLineToPrint(state){
    return state.lineToPrint
  },
  getPieToPrint(state){
    return state.PieToPrint
  },
  getExcelHeader(state){
    return state.excelHeader
  },
  getExcelData(state){
    return state.excelData
  },
  getCsvHeader(state){
    return state.csvHeader
  },
  getCsvData(state){
    return state.csvData
  },
  getMedia(state){
    return state.media
  },
  getMediaGambar(state){
    return state.mediaGambar
  },
  getMediaVideo(state){
    return state.mediaVideo
  }
}
