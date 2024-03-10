import pickle
import streamlit as st
import pandas as pd

# Membaca model
kbst_model = pickle.load(open('kbst_model.sav', 'rb'))

# Judul web
st.title('SISTEM PREDIKSI KELUARGA BERESIKO STUNTING')

# Membuat kolom dengan 2 bagian
col1, col2 = st.columns(2)

# Nilai default untuk setiap input
default_values = {
    'sumber_air_minum_buruk': '0',
    'sanitasi_buruk': '0',
    'terlalu_muda_istri': '0',
    'terlalu_tua_istri': '0',
    'terlalu_dekat_umur': '0',
    'terlalu_banyak_anak': '0'
}

# Input untuk pertanyaan-pertanyaan
with col1:
    sumber_air_minum_buruk = st.text_input('Apakah Sumber Air Minum Buruk? (0/1)', default_values['sumber_air_minum_buruk'])

with col2:
    sanitasi_buruk = st.text_input('Apakah Sanitasi Buruk? (0/1)', default_values['sanitasi_buruk'])

with col1:
    terlalu_muda_istri = st.text_input('Apakah Istri Terlalu Muda? (0/1)', default_values['terlalu_muda_istri'])

with col2:
    terlalu_tua_istri = st.text_input('Apakah Istri Terlalu Tua? (0/1)', default_values['terlalu_tua_istri'])

with col1:
    terlalu_dekat_umur = st.text_input('Apakah Umur Suami & Istri Terlalu Dekat? (0/1)', default_values['terlalu_dekat_umur'])

with col2:
    terlalu_banyak_anak = st.text_input('Apakah Memiliki Banyak Anak? (0/1)', default_values['terlalu_banyak_anak'])

# Variabel untuk hasil prediksi
kbst_diagnosis = ''

# Tombol untuk prediksi
if st.button('Lakukan Prediksi'):
    # Menggunakan model untuk melakukan prediksi
    input_data = {
        'sumber_air_minum_buruk': int(sumber_air_minum_buruk) if sumber_air_minum_buruk.isdigit() and int(sumber_air_minum_buruk) in [0, 1] else None,
        'sanitasi_buruk': int(sanitasi_buruk) if sanitasi_buruk.isdigit() and int(sanitasi_buruk) in [0, 1] else None,
        'terlalu_muda_istri': int(terlalu_muda_istri) if terlalu_muda_istri.isdigit() and int(terlalu_muda_istri) in [0, 1] else None,
        'terlalu_tua_istri': int(terlalu_tua_istri) if terlalu_tua_istri.isdigit() and int(terlalu_tua_istri) in [0, 1] else None,
        'terlalu_dekat_umur': int(terlalu_dekat_umur) if terlalu_dekat_umur.isdigit() and int(terlalu_dekat_umur) in [0, 1] else None,
        'terlalu_banyak_anak': int(terlalu_banyak_anak) if terlalu_banyak_anak.isdigit() and int(terlalu_banyak_anak) in [0, 1] else None,
    }

    # Jika ada nilai yang tidak valid, beri tahu pengguna
    if None in input_data.values():
        st.error('Masukkan hanya angka 0 atau 1.')
    else:
        # Membuat DataFrame dari input untuk memudahkan prediksi
        input_df = pd.DataFrame([input_data])

        kbst_prediction = kbst_model.predict(input_df)

        # Menyusun diagnosa berdasarkan hasil prediksi
        if kbst_prediction[0] == 1:
            kbst_diagnosis = 'Keluarga Beresiko Stunting'
        else:
            kbst_diagnosis = 'Keluarga Tidak Beresiko Stunting'

# Tombol reset untuk mengembalikan nilai ke default
if st.button('Reset'):
    sumber_air_minum_buruk = default_values['sumber_air_minum_buruk']
    sanitasi_buruk = default_values['sanitasi_buruk']
    terlalu_muda_istri = default_values['terlalu_muda_istri']
    terlalu_tua_istri = default_values['terlalu_tua_istri']
    terlalu_dekat_umur = default_values['terlalu_dekat_umur']
    terlalu_banyak_anak = default_values['terlalu_banyak_anak']

# Menampilkan hasil prediksi
st.success(f'Hasil Prediksi: {kbst_diagnosis}')
