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
    st.session_state.state['sumber_air_minum_buruk'] = st.selectbox('Apakah Sumber Air Minum Buruk?', ['Pilih', 'Ya', 'Tidak'], index=0 if st.session_state.state['sumber_air_minum_buruk'] == 'Pilih' else 1)

with col2:
    st.session_state.state['sanitasi_buruk'] = st.selectbox('Apakah Sanitasi Buruk?', ['Pilih', 'Ya', 'Tidak'], index=0 if st.session_state.state['sanitasi_buruk'] == 'Pilih' else 1)

with col1:
    st.session_state.state['terlalu_muda_istri'] = st.selectbox('Apakah Istri Terlalu Muda?', ['Pilih', 'Ya', 'Tidak'], index=0 if st.session_state.state['terlalu_muda_istri'] == 'Pilih' else 1)

with col2:
    st.session_state.state['terlalu_tua_istri'] = st.selectbox('Apakah Istri Terlalu Tua?', ['Pilih', 'Ya', 'Tidak'], index=0 if st.session_state.state['terlalu_tua_istri'] == 'Pilih' else 1)

with col1:
    st.session_state.state['terlalu_dekat_umur'] = st.selectbox('Apakah Umur Suami & Istri Terlalu Dekat?', ['Pilih', 'Ya', 'Tidak'], index=0 if st.session_state.state['terlalu_dekat_umur'] == 'Pilih' else 1)

with col2:
    st.session_state.state['terlalu_banyak_anak'] = st.selectbox('Apakah Memiliki Banyak Anak?', ['Pilih', 'Ya', 'Tidak'], index=0 if st.session_state.state['terlalu_banyak_anak'] == 'Pilih' else 1)

# Variabel untuk hasil prediksi
kbst_diagnosis = ''

# Tombol untuk prediksi
if st.button('Lakukan Prediksi'):
    # Labelling 'Ya' menjadi 1 dan 'Tidak' menjadi 0
    mapping = {'Ya': 1, 'Tidak': 0}

    # Menggunakan model untuk melakukan prediksi
    input_data = {key: mapping[value] if value in mapping else None for key, value in st.session_state.state.items()}

    # Jika ada nilai yang tidak valid, beri tahu pengguna
    if None in input_data.values():
        st.error('Pilih opsi yang valid.')

    else:
        # Membuat DataFrame dari input untuk memudahkan prediksi
        input_df = pd.DataFrame([input_data])

        kbst_prediction = kbst_model.predict(input_df)

        # Menyusun diagnosa berdasarkan hasil prediksi
        if kbst_prediction[0] == 1:
            kbst_diagnosis = 'Keluarga Beresiko Stunting'
        else:
            kbst_diagnosis = 'Keluarga Tidak Beresiko Stunting'

        # Mengatur state ke nilai default setelah prediksi
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
