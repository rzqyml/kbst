import pickle
import streamlit as st

# membaca model
kbst_model = pickle.load(open('kbst_model.sav', 'rb'))

# judul web
st.title('SISTEM PREDIKSI KELUARGA BERESIKO STUNTING')

# membuat kolom dengan 2 bagian
col1, col2 = st.columns(2)

# Input untuk pertanyaan-pertanyaan
with col1:
    sumber_air_minum_buruk = st.number_input('Apakah Sumber Air Minum Buruk?', step=1, value=1)

with col2:
    sanitasi_buruk = st.number_input('Apakah Sanitasi Buruk?', step=1, value=1)

with col1:
    terlalu_muda_istri = st.number_input('Apakah Istri Terlalu Muda?', step=1, value=1)

with col2:
    terlalu_tua_istri = st.number_input('Apakah Istri Terlalu Tua?', step=1, value=1)

with col1:
    terlalu_dekat_umur = st.number_input('Apakah Umur Suami & Istri Terlalu Dekat?', step=1, value=1)

with col2:
    terlalu_banyak_anak = st.number_input('Apakah Memiliki Banyak Anak?', step=1, value=1)

# variabel untuk hasil prediksi
kbst_diagnosis = ''

# membuat tombol untuk prediksi
if st.button('Test Prediksi Stunting'):
    # Menggunakan model untuk melakukan prediksi
    kbst_prediction = kbst_model.predict([[sumber_air_minum_buruk, sanitasi_buruk, terlalu_muda_istri, terlalu_tua_istri, terlalu_dekat_umur, terlalu_banyak_anak]])

    # Menyusun diagnosa berdasarkan hasil prediksi
    if kbst_prediction[0] == 1:
        kbst_diagnosis = 'Keluarga Beresiko Stunting'
    else:
        kbst_diagnosis = 'Keluarga Tidak Beresiko Stunting'

# tombol reset untuk mengembalikan nilai ke default
if st.button('Reset Input'):
    sumber_air_minum_buruk = default_values['sumber_air_minum_buruk']
    sanitasi_buruk = default_values['sanitasi_buruk']
    terlalu_muda_istri = default_values['terlalu_muda_istri']
    terlalu_tua_istri = default_values['terlalu_tua_istri']
    terlalu_dekat_umur = default_values['terlalu_dekat_umur']
    terlalu_banyak_anak = default_values['terlalu_banyak_anak']

# Menampilkan hasil diagnosa
st.success(kbst_diagnosis)
