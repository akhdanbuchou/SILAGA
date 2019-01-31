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
  setGangguanGol1(state,data){
      state.gangguanGol1 = data
  },
  setLineChart(state, data){
    state.lineToPrint = data
    var temp = []
    var min = []
    var max = []
    for(var i = 0; i < data.result.length; i++){
        max.push(Math.max.apply(null, data.result[i].jumlahPerInterval))
        min.push(Math.min.apply(null, data.result[i].jumlahPerInterval))
        var obj = {
            name: data.result[i].namaGangguan,
            data: data.result[i].jumlahPerInterval
        }
        temp.push(obj)
    }
    max = Math.max.apply(null, max)
    min = Math.min.apply(null, min)
    var maxBar = max + 2
    var minBar = 0
    if(min > 1){
        minBar = min - 2
    }
    state.lineData = temp

    state.lineChart = {
        chart: {
          shadow: {enabled: true, color: '#000', top: 18, left: 7, blur: 10, opacity: 1},
          toolbar: {show: false}
        },
        colors: ['rgb(0, 143, 251)', 'rgb(0, 227, 150)','rgb(254, 176, 25)','rgb(255, 69, 96)'
        ,'rgb(173, 31, 159)','rgb(56, 46, 55)'],
        dataLabels: {enabled: true},
        stroke: {curve: 'smooth'},
        title: {text: 'Rekapitulasi Berita Gangguan',align: 'left'},
        grid: {
          borderColor: '#e7e7e7',
          row: {colors: ['#f3f3f3', 'transparent'], opacity: 0.5}},
        markers: {size: 6},
        xaxis: {categories: data.axisx,title: {text: 'Tanggal'}},
        yaxis: {title: {text: 'Jumlah Berita'},min: minBar,max: maxBar},
        legend: {position: 'top',horizontalAlign: 'right',floating: true,offsetY: -25,offsetX: -5
        }
    }


  },
  setPieChart(state, data){
    state.PieToPrint = data
    if(data.selectedGangguan == '0'){
        var temp = []
        for(var i = 0; i < data.length; i++){
            temp.push(data[i].jumlahGangguan)
        }
        state.pieData = temp

        state.pieChart = {
            labels: ['Kejahatan', 'Pelanggaran', 'Gangguan', 'Bencana'],
            responsive: [{
                breakpoint: 480,
                options: {
                chart: {
                    width: 500
                },
                legend: {
                    position: 'bottom'
                }
                }
            }]
        }
    }else{
        var label = []
        var index = data.selectedGangguan - 1
        for(var i = 0; i < data.selectedCategory[index].subkategori2.length; i++){
            label.push(data.selectedCategory[index].subkategori2[i].kategori2)
        }
        
        var temp = []
        for(var i = 0; i < data.length; i++){
            temp.push(data[i].jumlahGangguan)
        }
        state.pieData = temp
        state.pieChart = {
            labels: label,
            responsive: [{
                breakpoint: 480,
                options: {
                chart: {
                    width: 500
                },
                legend: {
                    position: 'bottom'
                }
                }
            }]
        }
    }
    
  }

}
