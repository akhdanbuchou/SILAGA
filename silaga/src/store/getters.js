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
  }
}
