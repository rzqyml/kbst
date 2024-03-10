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
    'sumber_air_minum_buruk': 'Pilih',
    'sanitasi_buruk': 'Pilih',
    'terlalu_muda_istri': 'Pilih',
    'terlalu_tua_istri': 'Pilih',
    'terlalu_dekat_umur': 'Pilih',
    'terlalu_banyak_anak': 'Pilih'
}

# Inisialisasi session state jika belum ada
if 'reset_clicked' not in st.session_state:
    st.session_state.reset_clicked = False

# Input untuk pertanyaan-pertanyaan
with col1:
    # Simpan opsi dalam variabel
    sumber_air_minum_buruk_options = ['Ya', 'Tidak']
    # Gunakan variabel tersebut untuk menentukan indeks
    st.session_state.sumber_air_minum_buruk = st.selectbox('Apakah Sumber Air Minum Buruk?', sumber_air_minum_buruk_options, index=sumber_air_minum_buruk_options.index(st.session_state.sumber_air_minum_buruk) if st.session_state.sumber_air_minum_buruk in sumber_air_minum_buruk_options else 0)

# Lakukan hal yang sama untuk kolom lainnya...

# Tombol reset untuk mengembalikan nilai ke default
if st.button('Reset'):
    st.session_state.reset_clicked = True

# Jika tombol reset sudah ditekan, reset nilai
if st.session_state.reset_clicked:
    st.session_state.sumber_air_minum_buruk = default_values['sumber_air_minum_buruk']
    # Reset flag reset_clicked
    st.session_state.reset_clicked = False

# Lakukan hal yang sama untuk kolom lainnya...

# Membuat tombol untuk prediksi
if st.button('Lakukan Prediksi'):
    # Labelling 'Ya' menjadi 1 dan 'Tidak' menjadi 0
    mapping = {'Ya': 1, 'Tidak': 0}

    # Menggunakan model untuk melakukan prediksi
    input_data = {
        'sumber_air_minum_buruk': st.session_state.sumber_air_minum_buruk,
        # Menambahkan hal yang sama untuk kolom lainnya...
    }

    # Mengganti nilai 'Pilih' menjadi nilai kosong
    input_data = {key: '' if value == 'Pilih' else value for key, value in input_data.items()}

    # Melakukan mapping 'Ya' dan 'Tidak' ke 1 dan 0
    input_data_mapped = {key: mapping[value] for key, value in input_data.items()}

    # Membuat DataFrame dari input untuk memudahkan prediksi
    input_df = pd.DataFrame([input_data_mapped])

    kbst_prediction = kbst_model.predict(input_df)

    # Menyusun diagnosa berdasarkan hasil prediksi
    if kbst_prediction[0] == 1:
        kbst_diagnosis = 'Keluarga Beresiko Stunting'
    else:
        kbst_diagnosis = 'Keluarga Tidak Beresiko Stunting'

# Menampilkan hasil prediksi
st.success(f'Hasil Prediksi: {kbst_diagnosis}')
