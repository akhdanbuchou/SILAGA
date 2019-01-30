// https://vuex.vuejs.org/en/mutations.html

export default {
  setAllNews(state, data) {
      state.news = data
  },
  setAllUsers(state, data) {
      state.users = data
  },
  setCategories(state, data){
      state.categories = data
  },
  setRoles(state,data){
      state.roles = data
  },
  setCurrentRole(state,data){
      state.currentRole = data
  },
  setTelegramReport(state,data){
      state.telegram = data
  },
  setKeywordTable(state,data){
      state.keywordTable = data
  },
  setLineChart(state, data){
    console.log(data)
  },
  setPieChart(state, data){
    console.log(data)
  }
}
