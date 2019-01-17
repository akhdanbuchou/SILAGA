<template>
  <v-container
    fluid
    grid-list-sm
  >
    <v-layout>
      <v-flex>
        <material-card color="green darken-4" title="Analisis Linechart"> 
          <div id="chart">
            <apexchart type=line height=350 :options="chartOptionsLine" :series="seriesLine"/>
          </div>
        </material-card>
      </v-flex>  
    </v-layout>
    <v-layout>
      <v-flex xs6>
        <material-card color="green darken-4" title="Analisis Persebaran Gangguan">
          <v-spacer></v-spacer>
          <div style="width: 480px; height: 480px;" id="mapContainer"></div>
        </material-card>
      </v-flex>
      <v-flex xs6>
        <material-card color="green darken-4" title="Analisis Piechart">
          <v-spacer></v-spacer>
          <div id="chart" class="mx-5">
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

export default {
  components: {
    apexchart: VueApexCharts
  },
  data () {
    return {
      seriesLine: [
          {
            name: "High - 2013",
            data: [28, 29, 33, 36, 32, 32, 33]
          },
          {
            name: "Low - 2013",
            data: [12, 11, 14, 18, 17, 13, 13]
          }
        ],
        chartOptionsLine: {
          chart: {
            shadow: {
              enabled: true,
              color: '#000',
              top: 18,
              left: 7,
              blur: 10,
              opacity: 1
            },
            toolbar: {
              show: false
            }
          },
          colors: ['#77B6EA', '#545454'],
          dataLabels: {
            enabled: true,
          },
          stroke: {
            curve: 'smooth'
          },
          title: {
            text: 'Average High & Low Temperature',
            align: 'left'
          },
          grid: {
            borderColor: '#e7e7e7',
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
            },
          },
          markers: {
            
            size: 6
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            title: {
              text: 'Month'
            }
          },
          yaxis: {
            title: {
              text: 'Temperature'
            },
            min: 5,
            max: 40
          },
          legend: {
            position: 'top',
            horizontalAlign: 'right',
            floating: true,
            offsetY: -25,
            offsetX: -5
          }
        },

        seriesPie: [44, 55, 13, 43, 22],
        chartOptionsPie: {
          labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
          responsive: [{
            breakpoint: 480,
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
  },
  methods: {
    
  },
  mounted(){
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
        var places = ['Depok','Bontang','Medan', 'Ambon','Surabaya','Bandung','Makassar']

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
  }
}
</script>
