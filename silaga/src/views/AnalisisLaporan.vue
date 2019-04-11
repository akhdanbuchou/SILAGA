<template>
  <v-container
    fluid
    grid-list-sm
  >
    <v-layout>
      <v-flex>
        <v-card>
          <v-card-title xs12 sm12 md12 class="font-weight-medium">
            Filter Pencarian Analisis
            <v-spacer></v-spacer>
            <v-btn color="green lighten-1 " dark class="ml-3" 
              @click="applyFilter( 
                filterGangguan, filterKunci, filterStartDate, filterEndDate, filterFrekuensi)">
              Terapkan Filter
            </v-btn>
            <v-btn color="green darken-2" dark class="ml-3" @click="cetakAnalisis()">
              Cetak Analisis
            </v-btn>
            <download-excel
                class   ="v-btn green darken-2 ml-3"
                :data   ="excelData"
                :fields ="excelHeader"
                name    ="Rekap Analisis.xls">
                Unduh Excel
            </download-excel>
            <vue-csv-downloader
                class         ="v-btn green darken-2 ml-3"
                :data         ="csvData"
                :fields       ="csvHeader"
                download-name ="Rekap Analisis.csv">
                Unduh CSV
            </vue-csv-downloader>
          </v-card-title>
          <v-card-text>
            <v-layout>
              <v-flex xs6 sm6 md6>
                <v-select class="ml-2" :items="dropdownGangguan" v-model="filterGangguan"
                  item-text="text" item-value="value" label="Pilih Jenis Gangguan">
                </v-select>
              </v-flex>
              <v-flex xs6 sm6 md6>
                <v-text-field class="ml-4" v-model="filterKunci" label="Cari dengan Kata Kunci">
                </v-text-field>
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex xs4 sm4 md4>
                <v-menu class="ml-2" :close-on-content-click="false" v-model="menuDate1" :nudge-right="40"
                  lazy transition="scale-transition" offset-y full-width min-width="290px">
                  <v-text-field slot="activator" v-model="filterStartDate" label="Tanggal Mulai" readonly>
                  </v-text-field>
                  <v-date-picker dark v-model="filterStartDate" @input="menuDate1 = false"></v-date-picker>
                </v-menu>
              </v-flex>
              <v-flex xs4 sm4 md4>
                <v-menu class="ml-4" :close-on-content-click="false" v-model="menuDate2" :nudge-right="40"
                  lazy transition="scale-transition" offset-y full-width min-width="290px">
                  <v-text-field slot="activator" v-model="filterEndDate" label="Tanggal Berakhir" readonly>
                  </v-text-field>
                  <v-date-picker dark v-model="filterEndDate" @input="menuDate2 = false"></v-date-picker>
                </v-menu>
              </v-flex>
              <v-flex xs4 sm4 md4>
                <v-select
                  class="ml-4"
                  :items="dropdownFrekuensi"
                  v-model="filterFrekuensi"
                  item-text="text"
                  item-value="value"
                  label="Pilih Frekuensi Analisis"
                ></v-select>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>

        <v-dialog v-model="modalDetail" max-width="500px">
          <ModalDetailLaporan
          :selectedLaporan="selectedLaporan" 
          :modalDetail="modalDetail" v-on:closeDetail="closeDetail($event)"
          ></ModalDetailLaporan>
        </v-dialog>

        <material-card color="green darken-4" :title="titleLineChart"> 
          <v-progress-circular v-if="seriesLine.length == 0 || loadLineFlag" class="mb-3 ml-3"
              row wrap align-center justify-center
              :width="3"
              color="green"
              indeterminate
          ></v-progress-circular>
          <div v-else id="chart">
            <apexchart type=line height=350 :options="chartOptionsLine" :series="seriesLine"/>
          </div>
          
          <div v-if="popTable.length == 0 && loadPopTableFlag">Tidak ada berita</div>
          <div v-else-if="popTable.length != 0 && loadPopTableFlag">
            <v-card-title>
              <v-btn color="green darken-3" dark @click="closePopTable()">Tutup Tabel</v-btn>
              <v-spacer></v-spacer>
              <v-text-field
                  v-model="search"
                  label="Cari Berita"
              ></v-text-field>
              <v-icon>mdi-magnify</v-icon>
            </v-card-title>
            <v-data-table 
              :headers="headers"
              :items="popLaporan"
              :search="search"
            >
              <template slot="items" slot-scope="props">
                <td class="text-xs-left">{{ props.index + 1 }}</td>
                <td class="text-xs-left">{{ props.item.pelapor }}</td>
                <td class="text-xs-left">{{ props.item.kategori }}</td>
                <td class="text-xs-left">{{ props.item.tanggal }}</td>
                <td class="text-xs-left">{{ conciseNews(props.item.isi) }}</td>
                <td class="justify-left pl-3 layout px-0">
                  <v-icon 
                    small
                    class="mr-2"
                    @click="popDetail(props.item)"
                    color="blue"
                  >
                    mdi-feature-search-outline
                  </v-icon>
                </td>
              </template>
              <v-alert slot="no-results" :value="true" color="error" icon="mdi-warning">
                Your search for "{{ search }}" found no results.
              </v-alert>
            </v-data-table>
          </div>
        </material-card>
      </v-flex>  
    </v-layout>
    <v-layout>
      <v-flex xs12>
        <material-card color="green darken-4" :title="titlePieChart">
          <v-spacer></v-spacer>
          <v-progress-circular v-if="seriesPie.length == 0 || loadPieFlag" class="mb-3 ml-3"
              row wrap align-center justify-center
              :width="3"
              color="green"
              indeterminate
            ></v-progress-circular>
          <div v-else id="chart" class="mx-5">
            <apexchart type=pie :options="chartOptionsPie" :series="seriesPie" />
          </div>
          <v-card-text>
            <p>Piechart di atas menampilkan pembagian porsi gangguan berdasarkan jumlahnya</p>
          </v-card-text>
        </material-card>
      </v-flex>  
    </v-layout>
    
    
  </v-container>
</template>

<script>
import ModalDetailLaporan from "@/components/utilities/laporan/ModalDetailLaporan.vue";
import VueApexCharts from 'vue-apexcharts'
import VueCsvDownloader from 'vue-csv-downloader';
import { mapGetters } from 'vuex';
import axios from 'axios'
const defaultApi = "http://5.79.64.131:18880/"

export default {
  components: {
    ModalDetailLaporan,
    apexchart: VueApexCharts,
    VueCsvDownloader
  },
     data: () => ({
        modalDetail: false,
        selectedLaporan: {},
        titleLineChart:'Analisis Linechart Gangguan ',
        titlePieChart:'Analisis Piechart Gangguan ',
        titleMap:'Analisis Pesebaran Gangguan ',
        loadPieFlag: false,
        loadLineFlag: false,
        secondLayerFlag: false,
        menuDate1: false,
        menuDate2: false,
        search:'',
        showMap: false,
        map: [],
        selectedGangguan: '',
        filterGangguan: '0',
        filterKunci: '',
        filterStartDate: '',
        filterEndDate: '',
        filterFrekuensi: 'bulanan',
        filterMap:'1',
        headers: [
          { text: 'No', value:'no'},
          { text: 'Pelapor', value: 'pelapor' },
          { text: 'Kategori', value: 'kategori' },
          { text: 'Waktu Lapor', value: 'timestamp' },
          { text: 'Isi', value: 'content' },
          { text: '', value: 'action'}
        ],
        dropdownFrekuensi:[
          {
            text:'Harian',
            value:'harian'
          },
          {
            text:'Mingguan',
            value:'mingguan'
          },
          {
            text:'Bulanan',
            value:'bulanan'
          },
          {
            text:'Tahunan',
            value:'tahunan'
          }
        ]
    }),
    methods: {
      popDetail(laporan){
        this.selectedLaporan = laporan
        this.modalDetail = true
      },
      closeDetail(event){
        this.modalDetail = event
      },
      closePopTable(){
        this.$store.commit('setLoadPopTableLaporanFlag',false)
      },
      conciseNews(text){
        var result = text.substring(0,120) + "..."
        return result
      },
      cetakAnalisis(){
        axios({
          method: 'post',
          url: defaultApi + 'cetak',
          data:{
            linedata: this.lineToPrint,
            piedata: this.pieToPrint 
          },
          responseType:'arraybuffer'
        }).then(response => {
          const url = window.URL.createObjectURL(new Blob([response.data]))
          const link = document.createElement('a')
          link.href = url
          link.setAttribute('download', 'lapor.docx')
          document.body.appendChild(link)
          link.click()
        })

      },
      applyFilter(filterGangguan, filterKunci, filterStartDate, filterEndDate, filterFrekuensi){
        this.$store.commit('setLoadPopTableFlag',false)
        this.$store.commit('setFrekuensiRekap',filterFrekuensi)

        if(filterGangguan != '0'){
          this.$store.commit('setFlagLayer1', true)
          this.$store.commit('setFilterLayer1', filterGangguan)
        }else{
          this.$store.commit('setFlagLayer1', false)
          this.$store.commit('setFilterLayer1', '')
        }

        this.loadLineFlag = true
        this.loadPieFlag = true

        if(filterStartDate == ''){
          filterStartDate = '-'
        }
        if(filterEndDate == ''){
          filterEndDate = '-'
        }
        if(filterKunci == ''){
          filterKunci = '-'
        }
        this.selectedGangguan = filterGangguan

        axios({
          method: 'get',
          url: defaultApi + 'rekap-telegram/'+ filterGangguan +'/'+ filterStartDate +
          '/'+ filterEndDate +'/'+ filterKunci +'/'+ filterFrekuensi
        }).then(response => {
          if(response){
            this.$store.commit('setLineChart',response.data)
            this.loadLineFlag = false
          }
        })

        axios({
          method: 'get',
          url: defaultApi + 'pie-chart-telegram/'+ filterGangguan +'/'+ filterStartDate +
          '/'+ filterEndDate +'/'+ filterKunci
        }).then(response => {
          if(response){
            response.data.selectedCategory = this.gangguanGol1
            response.data.selectedGangguan = this.selectedGangguan
            this.$store.commit('setPieChart',response.data)
            this.loadPieFlag = false
          }
        })

        var gangguan = ''
        var tLinechart = ''
        var tPiechart = ''
        var tMap = ''
        if(filterGangguan == '0'){gangguan = ''}
        else if(filterGangguan == '1'){gangguan = "Kejahatan"}
        else if(filterGangguan == '2'){gangguan = "Pelanggaran"}
        else if(filterGangguan == '3'){gangguan = ""}
        else if(filterGangguan == '4'){gangguan = "Bencana"}

        tLinechart = 'Analisis Linechart Gangguan ' + gangguan
        tPiechart = 'Analisis Piechart Gangguan ' + gangguan
        tMap = 'Analisis Pesebaran Gangguan ' + gangguan

        this.titleLineChart = tLinechart
        this.titlePieChart = tPiechart
        this.titleMap = tMap
      }
    },
    computed: {
      ...mapGetters({
          seriesLine:'getLineData',
          chartOptionsLine:'getLineChart',
          seriesPie:'getPieData',
          chartOptionsPie:'getPieChart',
          gangguanGol1:'getGangguanGol1',
          lineToPrint:'getLineToPrint',
          pieToPrint:'getPieToPrint',
          excelHeader:'getExcelHeader',
          excelData:'getExcelData',
          csvHeader:'getCsvHeader',
          csvData:'getCsvData',
          popTable: 'getPopTableLaporan',
          loadPopTableFlag: 'getLoadPopTableLaporanFlag'
      }),
      dropdownGangguan(){
        var result = []
        var standar = {
          text: 'semua',
          value: '0'
        }
        result.push(standar)
        for(var i = 0; i < this.gangguanGol1.length; i++){
          var temp = {
            text: this.gangguanGol1[i].kategori1,
            value: this.gangguanGol1[i].id
          }
          result.push(temp)
        }
        return result
      },
      popLaporan(){
        var result = []
        var tempResult
        for(var i = 0; i< this.popTable.length; i++){
          var tempKategori = ""
          var toLoopKategori = this.popTable[i].kategori

          for(var j = 0; j < toLoopKategori.length; j++){
              if(toLoopKategori.length - j == 1){
                tempKategori += this.popTable[i].kategori[j]
              }else{
                tempKategori += this.popTable[i].kategori[j] + " - "
              }
          }
          tempResult = {
            id: this.popTable[i].id,
            pelapor: this.popTable[i].pelapor[0],
            kategori: tempKategori,
            tanggal: this.popTable[i].date.substring(0,10),
            isi: this.popTable[i].laporan[0]
          }
          result.push(tempResult)

        }
        return result
      }
    },
    mounted(){
      this.$store.dispatch('getDefaultTelegramLineChart')
      this.$store.dispatch('getDefaultTelegramPieChart')
      this.$store.dispatch('getFirstCategories')     
    
    }
}
</script>
