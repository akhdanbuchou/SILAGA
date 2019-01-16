<template>
  <v-container
    fill-height
    fluid
    grid-list-xl
  >
    <v-layout
      justify-center
      wrap
    >
      <v-flex
        md12
      >
        <v-card>
          <v-card-title class="font-weight-medium">
            Daftar Laporan Lapangan Telegram
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
            <v-icon>mdi-magnify</v-icon>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="laporan"
            :search="search"
          >
            <template slot="items" slot-scope="props">
              <td>{{ props.item.no }}</td>
              <td class="text-xs-left">{{ props.item.pengirim }}</td>
              <td class="text-xs-left">{{ props.item.kategori }}</td>
              <td class="text-xs-left">{{ props.item.lokasi }}</td>
              <td class="text-xs-left">{{ props.item.waktu }}</td>
              <td class="text-xs-left">{{ props.item.isi }}</td>
            </template>
            <v-alert slot="no-results" :value="true" color="error" icon="mdi-warning">
              Your search for "{{ search }}" found no results.
            </v-alert>
          </v-data-table>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    search: '',
    headers: [
      {text: 'No',value: 'no'},
      { text: 'Pengirim', value: 'pengirim' },
      { text: 'Kategori', value: 'kategori' },
      { text: 'Lokasi', value: 'lokasi' },
      { text: 'Waktu', value: 'waktu' },
      { text: 'Isi Laporan', value: 'isi' }
    ],
    laporan: [
          {
            value: false,
            no: '1',
            pengirim: 'Aejo Legowo',
            kategori: 'Pencurian',
            lokasi: 'Jakarta Utara',
            waktu: '10/10/2018',
            isi:'Terjadi pencurian di wilayah pluit'
          },
          {
            value: false,
            no: '2',
            pengirim: 'Bejo Legowo',
            kategori: 'Pencurian',
            lokasi: 'Bandung',
            waktu: '10/10/2018',
            isi:'Terjadi pencurian di wilayah bandung'
          },
          {
            value: false,
            no: '3',
            pengirim: 'Cejo Legowo',
            kategori: 'Pencurian',
            lokasi: 'Nganjuk',
            waktu: '10/10/2018',
            isi:'Terjadi pencurian di wilayah nganjuk'
          },
          {
            value: false,
            no: '4',
            pengirim: 'Dejo Legowo',
            kategori: 'Pencurian',
            lokasi: 'Medan',
            waktu: '10/10/2018',
            isi:'Terjadi pencurian di wilayah medan, komandan'
          },
          
        ]
  })
}
</script>
