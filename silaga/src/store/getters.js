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
  }
}
