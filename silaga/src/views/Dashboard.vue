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
            <v-btn color="green lighten-1 " dark class="ml-3 ml-3" 
              @click="applyFilter( 
                filterGangguan, filterKunci, filterStartDate, filterEndDate, filterFrekuensi)">
              Terapkan Filter
            </v-btn>
            <v-btn color="green darken-2" dark class="ml-3 ml-3" @click="cetakAnalisis()">
              Cetak Analisis
            </v-btn>
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
        </material-card>
      </v-flex>  
    </v-layout>
    <v-layout>
      <v-flex xs6>
        <material-card color="green darken-4" :title="titleMap">
          <v-btn color="green darken-2" dark class="ml-3 ml-3" @click="loadMap(filterGangguan, 
          filterKunci, filterStartDate, filterEndDate)">
              Tampilkan Map
          </v-btn>
          <v-spacer></v-spacer>
          <div v-if="showMap" style="width: 480px; height: 480px;" id="mapContainer"></div>
          <div v-else style="width: 480px; height: 480px;" id="mapContainer"></div>
        </material-card>
      </v-flex>
      <v-flex xs6>
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

import VueApexCharts from 'vue-apexcharts'
import { mapGetters } from 'vuex';
import axios from 'axios'
const defaultApi = 'http://127.0.0.1:5000/'

export default {
  components: {
    apexchart: VueApexCharts
  },
    data () {
      return {
        titleLineChart:'Analisis Linechart Gangguan ',
        titlePieChart:'Analisis Piechart Gangguan ',
        titleMap:'Analisis Pesebaran Gangguan ',
        loadPieFlag: false,
        loadLineFlag: false,
        secondLayerFlag: false,
        menuDate1: false,
        menuDate2: false,
        showMap: false,
        map: [],
        selectedGangguan: '',
        filterGangguan: '0',
        filterKunci: '',
        filterStartDate: '',
        filterEndDate: '',
        filterFrekuensi: 'bulanan',
        filterMap:'1',
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
      }
    },
    methods: {
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
        document.getElementById('mapContainer').innerHTML = ''
        this.showMap = false

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
          url: defaultApi + 'rekap/'+ filterGangguan +'/'+ filterStartDate +
          '/'+ filterEndDate +'/'+ filterKunci +'/'+ filterFrekuensi
        }).then(response => {
          if(response){
            this.$store.commit('setLineChart',response.data)
            this.loadLineFlag = false
          }
        })

        axios({
          method: 'get',
          url: defaultApi + 'pie-chart/'+ filterGangguan +'/'+ filterStartDate +
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
      },
      loadMap(filterGangguan, filterKunci, filterStartDate, filterEndDate){
        this.showMap = true
        if(filterStartDate == ''){
          filterStartDate = '-'
        }
        if(filterEndDate == ''){
          filterEndDate = '-'
        }
        if(filterKunci == ''){
          filterKunci = '-'
        }
        var platform = new H.service.Platform({
          'app_id': 'MoO52514bDjIGMcKnyvl',
          'app_code': 'Wog4qWYDldsEqg45tk223Q'
        });

        // Retrieve the target element for the map:
        var targetElement = document.getElementById('mapContainer');

        // Obtain the default map types from the platform object
        var defaultLayers = platform.createDefaultLayers();

        // Instantiate (and display) a map object:
        var map = new H.Map(
        document.getElementById('mapContainer'),
        defaultLayers.normal.map,
        {
            zoom: 4.5,
            center: { lng: 113.9213, lat: 0.7893 } // Indonesia coord as center
        });

        // Enable the event system on the map instance:
        var mapEvents = new H.mapevents.MapEvents(map);

        // Instantiate the default behavior, providing the mapEvents object: 
        var behavior = new H.mapevents.Behavior(mapEvents);

        // Create the default UI:
        var ui = H.ui.UI.createDefault(map, defaultLayers, 'en-US');
        
        // lokasi lokasi didapat dari query python ke solr 
        axios.get(defaultApi + 'map/'+filterGangguan+'/'+filterStartDate+'/'+filterEndDate+'/'+filterKunci)
        .then(response => {
            this.map = response.data
            var places = this.map

            for (var i = 0; i <= places.length; i++) {
                // Looping through places defined by Indriya 
            
                // Create the parameters for the geocoding request:
                var geocodingParams = {
                    searchText: places[i]
                };

                // Define a callback function to process the geocoding response:
                var onResult = function(result) {
                    var locations = result.Response.View[0].Result,
                        position,
                        marker;

                    // Add a marker for each location found
                    for (i = 0;  i < locations.length; i++) {
                        position = {
                            lat: locations[i].Location.DisplayPosition.Latitude,
                            lng: locations[i].Location.DisplayPosition.Longitude
                        };
                        marker = new H.map.Marker(position);
                        map.addObject(marker);
                    }

                };
                
                // Get an instance of the geocoding service:
                var geocoder = platform.getGeocodingService();
                
                // Call the geocode method with the geocoding parameters,
                // the callback and an error callback function (called if a
                // communication error occurs):
                geocoder.geocode(geocodingParams, onResult, function(e) {
                    alert(e);
                });
            }
        }) 
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
          pieToPrint:'getPieToPrint'
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
      }
    },
    mounted(){
      this.$store.dispatch('getDefaultLineChart')
      this.$store.dispatch('getDefaultPieChart')
      this.$store.dispatch('getFirstCategories')     
    
    }
}
</script>
