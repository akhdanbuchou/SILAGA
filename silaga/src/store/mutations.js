// https://vuex.vuejs.org/en/mutations.html
import axios from 'axios';

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
  setFrekuensiRekap(state,data){
        state.frekuensiRekap = data
  },
  setFlagLayer1(state,data){
        state.flagLayer1 = data
  },
  setFilterLayer1(state,data){
        state.filterLayer1 = data
  },
  setLoadPopTableFlag(state, data){
        state.loadPopTableFlag = data
  },
  setMedia(state, data){
      if(state.mediaGambar.length == 0){
        Array.prototype.push.apply(state.mediaGambar, data.list_gambar)
        Array.prototype.push.apply(state.media, data.list_gambar)
      }else{
        state.mediaGambar = []
        Array.prototype.push.apply(state.mediaGambar, data.list_gambar)
        Array.prototype.push.apply(state.media, data.list_gambar)
      }

      if(state.mediaVideo.length == 0){
        Array.prototype.push.apply(state.mediaVideo, data.list_rekaman)
        Array.prototype.push.apply(state.media, data.list_rekaman)
      }else{
        state.mediaVideo = []
        Array.prototype.push.apply(state.mediaVideo, data.list_rekaman)
        Array.prototype.push.apply(state.media, data.list_rekaman)
      }
  },
  emptyMedia(state){
      state.media = []
      state.mediaGambar = []
      state.mediaVideo = []
  },
  setLineChart(state, data){
    var frek = 'bulanan'
    if(state.frekuensiRekap != 'bulanan' && state.frekuensiRekap != ''){
        frek = state.frekuensiRekap
    }

    state.lineToPrint = data
    var tempLine = []
    var tempHeaderExcel = {
        Jenis: "jenis"
    }
    var tempHeaderCsv = []
    tempHeaderCsv.push('id')
    tempHeaderCsv.push('jenis')
    var tempDataExcel = []
    var tempDataCsv = []
    var min = []
    var max = []

    for(var i = 0; i < data.result.length; i++){
        max.push(Math.max.apply(null, data.result[i].jumlahPerInterval))
        min.push(Math.min.apply(null, data.result[i].jumlahPerInterval))

        var obj = {
            name: data.result[i].namaGangguan,
            data: data.result[i].jumlahPerInterval
        }
        tempLine.push(obj)
    }

    max = Math.max.apply(null, max)
    min = Math.min.apply(null, min)
    var maxBar = max + 2
    var minBar = 0
    if(min > 1){
        minBar = min - 2
    }
    state.lineData = tempLine
    state.dateFilter = data.axisx
    state.lineChart = {
        tooltip:{
            intersect: true,
            shared: false
        },
        chart: {
            shadow: {enabled: true, color: '#000', top: 18, left: 7, blur: 10, opacity: 1},
            toolbar: {show: false},
            events: {
                dataPointSelection: function(event, chartContext, config) {

                    var date = state.dateFilter[config.dataPointIndex]
                    var nextDate = state.dateFilter[config.dataPointIndex + 1]
                    if(state.filterLayer1 == ''){
                        var kodeGangguan = config.seriesIndex + 1
                        axios.get('http://5.79.64.131:18880/detail-rekap/' + kodeGangguan
                                + '/' + date + '/' + frek)
                        .then(response => {
                            state.popTable = response.data
                            state.loadPopTableFlag = true
                        })
                    }else{
                        
                        var kodeGangguan = state.filterLayer1
                        axios.get('http://5.79.64.131:18880/detail-rekap/' + kodeGangguan
                                + '/' + date + '/' + frek)
                        .then(response => {

                            state.loadPopTableFlag = true
                            var tempArray = []
                            var indexLayer1 = state.filterLayer1 - 1
                            var indexLayer2 = config.seriesIndex

                            for(var i = 0; i < response.data.length; i++){
                                if(response.data[i].kategori[1] == state.gangguan[indexLayer1].sublayer[indexLayer2]){
                                    tempArray.push(response.data[i])
                                }
                            }
                            state.popTable = tempArray
                        })
                    }
                    

                    
                    
                    
                }
            }
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
        legend: {position: 'top',horizontalAlign: 'right',floating: true,offsetY: -25,offsetX: -5}
    }

    for(var i = 0; i < data.result.length; i++){
        var tempExcelData = {}
        var tempCsvData = {}
        tempExcelData.jenis = data.result[i].namaGangguan
        tempCsvData.jenis = data.result[i].namaGangguan
        tempCsvData.id = i + 1
        for(var j = 0; j < data.axisx.length; j ++){
            var headCount = 1
            
            var inCount = j + headCount
            tempHeaderExcel[data.axisx[j]] = 'header' + inCount
            headCount++
            tempExcelData['header' + inCount] = data.result[i].jumlahPerInterval[j]
            tempCsvData[data.axisx[j]] = data.result[i].jumlahPerInterval[j]
        }
        tempDataExcel.push(tempExcelData)
        tempDataCsv.push(tempCsvData)
    }

    for(var i = 0; i < data.axisx.length; i++){
        tempHeaderCsv.push(data.axisx[i])
    }
    state.csvData = tempDataCsv
    state.csvHeader = tempHeaderCsv
    state.excelData = tempDataExcel
    state.excelHeader = tempHeaderExcel   

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
                breakpoint: 300,
                options: {
                chart: {
                    width: 200
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
                breakpoint: 300,
                options: {
                chart: {
                    width: 200
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
