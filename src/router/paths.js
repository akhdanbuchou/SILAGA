/**
 * Define all of your application routes here
 * for more information on routes, see the
 * official documentation https://router.vuejs.org/en/
 */
export default [
  {
    path: '/login',
    name: 'Login',
    view: 'Login'
  },
  {
    path: '/',
    name: 'Dashboard Analisis',
    view: 'Dashboard'
  },
  {
    path: '/detail-berita',
    name: 'Detail Berita',
    view: 'DetailBerita'
  },
  {
    path: '/laporan-lapangan',
    name: 'Laporan Lapangan',
    view: 'LaporanLapangan'
  },
  {
    path: '/konfigurasi',
    name: 'Konfigurasi Sistem',
    view: 'Konfigurasi'
  }
]
