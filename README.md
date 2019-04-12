# eCEOS SILAGA API

SILAGA memberikan layanan untuk mengambil data Online Media, Online Media Classified, serta Telegram dari aplikasi Solr eCEOS.

## Getting Started

- Install Flask dari [Official Flask](http://flask.pocoo.org/docs/1.0/installation/)
- Buat virtual environment

* Aktifkan virtual environment dengan:
  '<nama folder environtment>/Script/activate'
  contoh:
  'env/Script/activate'

- Install dependency:
  'pip install -r requirements.txt'
- Jalankan dengan:
  'python main_rest.py'

### Documentation

[API SILAGA](https://docs.google.com/spreadsheets/d/1Y7nJvmuK078qtfuhtgxIEIjU4i2mADjVHESUNkx6I14/edit#gid=0)

## Deployment

- Akses server dengan WinSCP
- Copy file dari lokal ke server
- Sebelum menjalankan aplikasi pada server, **kill** proses aplikasi yang sama yang sedang berjalan pada server
- Jalankan dengan aplikasi dengan:
  'python main_rest.py'

## Built With

- [Flask](http://flask.pocoo.org/docs/1.0/installation/) - The web framework used
