import pickle
import streamlit as st
import pandas as pd

# membaca model
kbst_model = pickle.load(open('kbst_model.sav', 'rb'))

# judul web
st.title('SISTEM PREDIKSI KELUARGA BERESIKO STUNTING')

# membuat kolom dengan 2 bagian
col1, col2 = st.columns(2)

# nilai default untuk setiap input
default_values = {
    'sumber_air_minum_buruk': 'Pilih',
    'sanitasi_buruk': 'Pilih',
    'terlalu_muda_istri': 'Pilih',
    'terlalu_tua_istri': 'Pilih',
    'terlalu_dekat_umur': 'Pilih',
    'terlalu_banyak_anak': 'Pilih'
}

# Input untuk pertanyaan-pertanyaan
with col1:
    sumber_air_minum_buruk = st.selectbox('Apakah Sumber Air Minum Buruk?', ['Pilih', 'Ya', 'Tidak'])

with col2:
    sanitasi_buruk = st.selectbox('Apakah Sanitasi Buruk?', ['Pilih', 'Ya', 'Tidak'])

with col1:
    terlalu_muda_istri = st.selectbox('Apakah Istri Terlalu Muda?', ['Pilih', 'Ya', 'Tidak'])

with col2:
    terlalu_tua_istri = st.selectbox('Apakah Istri Terlalu Tua?', ['Pilih', 'Ya', 'Tidak'])

with col1:
    terlalu_dekat_umur = st.selectbox('Apakah Umur Suami & Istri Terlalu Dekat?', ['Pilih', 'Ya', 'Tidak'])

with col2:
    terlalu_banyak_anak = st.selectbox('Apakah Memiliki Banyak Anak?', ['Pilih', 'Ya', 'Tidak'])

# variabel untuk hasil prediksi
kbst_diagnosis = ''

# membuat tombol untuk prediksi
if st.button('Lakukan Prediksi'):
    # labelling 'Ya' menjadi 1 dan 'Tidak' menjadi 0
    mapping = {'Ya': 1, 'Tidak': 0}

    # menggunakan model untuk melakukan prediksi
    input_data = {
        'sumber_air_minum_buruk': sumber_air_minum_buruk,
        'sanitasi_buruk': sanitasi_buruk,
        'terlalu_muda_istri': terlalu_muda_istri,
        'terlalu_tua_istri': terlalu_tua_istri,
        'terlalu_dekat_umur': terlalu_dekat_umur,
        'terlalu_banyak_anak': terlalu_banyak_anak
    }

    # mengganti nilai 'Pilih' menjadi nilai kosong
    input_data = {key: '' if value == 'Pilih' else value for key, value in input_data.items()}

    # melakukan mapping 'Ya' dan 'Tidak' ke 1 dan 0
    input_data_mapped = {key: mapping[value] for key, value in input_data.items()}

    # membuat dataframe dari input untuk memudahkan prediksi
    input_df = pd.DataFrame([input_data_mapped])

    kbst_prediction = kbst_model.predict(input_df)

    #menyusun diagnosa berdasarkan hasil prediksi
    if kbst_prediction[0] == 1:
        kbst_diagnosis = 'Keluarga Beresiko Stunting'
    else:
        kbst_diagnosis = 'Keluarga Tidak Beresiko Stunting'

# tombol reset untuk mengembalikan nilai ke default
if st.button('Reset'):
    sumber_air_minum_buruk = default_values['sumber_air_minum_buruk']
    sanitasi_buruk = default_values['sanitasi_buruk']
    terlalu_muda_istri = default_values['terlalu_muda_istri']
    terlalu_tua_istri = default_values['terlalu_tua_istri']
    terlalu_dekat_umur = default_values['terlalu_dekat_umur']
    terlalu_banyak_anak = default_values['terlalu_banyak_anak']

# menampilkan hasil prediksi
st.success(f'Hasil Prediksi: {kbst_diagnosis}')
