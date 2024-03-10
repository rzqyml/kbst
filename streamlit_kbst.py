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
    'sumber_air_minum_buruk': 0,
    'sanitasi_buruk': 0,
    'terlalu_muda_istri': 0,
    'terlalu_tua_istri': 0,
    'terlalu_dekat_umur': 0,
    'terlalu_banyak_anak': 0
}

# Mengecek dan menginisialisasi state jika belum ada
if 'state' not in st.session_state:
    st.session_state.state = {
        'sumber_air_minum_buruk': default_values['sumber_air_minum_buruk'],
        'sanitasi_buruk': default_values['sanitasi_buruk'],
        'terlalu_muda_istri': default_values['terlalu_muda_istri'],
        'terlalu_tua_istri': default_values['terlalu_tua_istri'],
        'terlalu_dekat_umur': default_values['terlalu_dekat_umur'],
        'terlalu_banyak_anak': default_values['terlalu_banyak_anak']
    }

# Input untuk pertanyaan-pertanyaan
with col1:
    st.session_state.state['sumber_air_minum_buruk'] = st.selectbox('Apakah Sumber Air Minum Buruk?', [0, 1], index=default_values['sumber_air_minum_buruk'])

with col2:
    st.session_state.state['sanitasi_buruk'] = st.selectbox('Apakah Sanitasi Buruk?', [0, 1], index=default_values['sanitasi_buruk'])

with col1:
    st.session_state.state['terlalu_muda_istri'] = st.selectbox('Apakah Istri Terlalu Muda?', [0, 1], index=default_values['terlalu_muda_istri'])

with col2:
    st.session_state.state['terlalu_tua_istri'] = st.selectbox('Apakah Istri Terlalu Tua?', [0, 1], index=default_values['terlalu_tua_istri'])

with col1:
    st.session_state.state['terlalu_dekat_umur'] = st.selectbox('Apakah Umur Suami & Istri Terlalu Dekat?', [0, 1], index=default_values['terlalu_dekat_umur'])

with col2:
    st.session_state.state['terlalu_banyak_anak'] = st.selectbox('Apakah Memiliki Banyak Anak?', [0, 1], index=default_values['terlalu_banyak_anak'])

# Variabel untuk hasil prediksi
kbst_diagnosis = ''

# Tombol untuk prediksi
if st.button('Lakukan Prediksi'):
    # Menggunakan model untuk melakukan prediksi
    input_data = {key: value for key, value in st.session_state.state.items()}

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
    # Session state untuk menyimpan data sementara hasil inputan
    st.session_state.state = {
        'sumber_air_minum_buruk': default_values['sumber_air_minum_buruk'],
        'sanitasi_buruk': default_values['sanitasi_buruk'],
        'terlalu_muda_istri': default_values['terlalu_muda_istri'],
        'terlalu_tua_istri': default_values['terlalu_tua_istri'],
        'terlalu_dekat_umur': default_values['terlalu_dekat_umur'],
        'terlalu_banyak_anak': default_values['terlalu_banyak_anak']
    }

# Menampilkan hasil prediksi
st.success(f'Hasil Prediksi: {kbst_diagnosis}')
