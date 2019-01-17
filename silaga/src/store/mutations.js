// https://vuex.vuejs.org/en/mutations.html

export default {
  setAllNews(state, data) {
      state.news = data
      console.log(state.news)
  },
  setAllUsers(state, data) {
      state.users = data
      console.log(state.users)
  }
}
