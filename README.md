# 🚲 Proyek Analisis Data: Bike Sharing Dataset

Dashboard ini merupakan hasil analisis data peminjaman sepeda untuk periode 2011–2012. Proyek ini bertujuan untuk mengeksplorasi tren waktu, pengaruh faktor cuaca, serta pola aktivitas harian guna memberikan wawasan yang dapat mendukung pengelolaan operasional penyewaan sepeda.

---

## 📂 Struktur Direktori
- **dashboard/**: Berisi file utama aplikasi `dashboard.py` serta data yang telah dibersihkan (`main_data.csv` dan `hour_data.csv`)
- **data/**: Berisi dataset mentah asli (`day.csv` dan `hour.csv`) dari UCI Machine Learning Repository
- **notebook.ipynb**: Dokumentasi proses analisis data mulai dari *Data Wrangling*, *Exploratory Data Analysis (EDA)*, hingga visualisasi
- **requirements.txt**: Daftar library Python yang dibutuhkan untuk menjalankan proyek
- **README.md**: Dokumentasi lengkap proyek
- **url.txt**: Berisi alamat URL lokal untuk mengakses dashboard

---

## ❓ Pertanyaan Bisnis
1. Bagaimana tren jumlah peminjaman sepeda dari bulan ke bulan selama periode 2011–2012, dan pada musim apa permintaan paling tinggi?  
2. Bagaimana pengaruh kondisi cuaca dan suhu terhadap jumlah total peminjaman sepeda?  
3. Pada jam berapa peminjaman sepeda paling tinggi, dan apakah terdapat perbedaan pola antara hari kerja dan hari libur?  

---

## 🛠️ Cara Menjalankan

### 1. Instalasi Library
Pastikan semua dependensi telah terpasang dengan menjalankan:

```bash
pip install -r requirements.txt

### 2. Menjalankan Dashboard
Jalankan aplikasi Streamlit dengan perintah berikut:

```bash
streamlit run dashboard/dashboard.py

---

## 🌐 Akses Dashboard
Dashboard dapat diakses secara lokal melalui:  
http://localhost:8509/

---

## 🔍 Insight Utama
- **Tren Tahunan**: Terdapat peningkatan jumlah pengguna yang signifikan dari tahun 2011 ke tahun 2012.  
- **Pengaruh Musim**: Musim Fall (gugur) memiliki rata-rata peminjaman harian tertinggi dibandingkan musim lainnya.  
- **Kondisi Cuaca**: Cuaca cerah dengan suhu hangat (kisaran 20–30°C) menunjukkan korelasi positif yang kuat terhadap tingginya volume peminjaman.  
- **Pola Aktivitas Pengguna**: Pada hari kerja, puncak peminjaman terjadi pada jam sibuk pagi (08.00) dan sore (17.00), sedangkan pada hari libur pola peminjaman cenderung lebih merata dan terpusat di siang hari.  

---

## 📊 Output
Dashboard interaktif ini menampilkan:
- Tren peminjaman sepeda dari waktu ke waktu  
- Pengaruh kondisi cuaca dan suhu terhadap jumlah peminjaman  
- Pola peminjaman berdasarkan jam dan jenis hari (hari kerja vs hari libur)