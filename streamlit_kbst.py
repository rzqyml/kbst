import pickle
import streamlit as st
import pandas as pd

# Membaca model
kbst_model = pickle.load(open('kbst_model.sav', 'rb'))

# Judul web
st.title('SISTEM PREDIKSI KELUARGA BERESIKO STUNTING')

# Membuat kolom dengan 3 bagian
col1, col2, col3 = st.columns(3)

# Nilai default untuk setiap input
default_values = {
    'sumber_air_minum_buruk': '0',
    'sanitasi_buruk': '0',
    'terlalu_muda_istri': '0',
    'terlalu_tua_istri': '0',
    'terlalu_dekat_umur': '0',
    'terlalu_banyak_anak': '0'
}

# Mengecek dan menginisialisasi state jika belum ada
if 'reset_flag' not in st.session_state:
    st.session_state.reset_flag = False

if 'state' not in st.session_state:
    st.session_state.state = {
        'sumber_air_minum_buruk': default_values['sumber_air_minum_buruk'],
        'sanitasi_buruk': default_values['sanitasi_buruk'],
        'terlalu_muda_istri': default_values['terlalu_muda_istri'],
        'terlalu_tua_istri': default_values['terlalu_tua_istri'],
        'terlalu_dekat_umur': default_values['terlalu_dekat_umur'],
        'terlalu_banyak_anak': default_values['terlalu_banyak_anak']
    }

# List untuk menyimpan data input dan hasil prediksi
input_results = []

# Tombol untuk prediksi
if st.button('Lakukan Prediksi'):
    # Menggunakan model untuk melakukan prediksi
    input_data = {key: int(value) if value.isdigit() and int(value) in [0, 1] else None for key, value in st.session_state.state.items()}

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

        # Mengatur flag reset menjadi False setelah prediksi
        st.session_state.reset_flag = False

        # Menyimpan data input dan hasil prediksi ke dalam list
        input_result = st.session_state.state.copy()
        input_result['Hasil Prediksi'] = kbst_diagnosis
        input_results.append(input_result)

# Tombol reset untuk mengembalikan nilai ke default
if st.button('Reset'):
    # Jika flag reset adalah False, atur state sesuai dengan nilai default
    if not st.session_state.reset_flag:
        st.session_state.state = {
            'sumber_air_minum_buruk': default_values['sumber_air_minum_buruk'],
            'sanitasi_buruk': default_values['sanitasi_buruk'],
            'terlalu_muda_istri': default_values['terlalu_muda_istri'],
            'terlalu_tua_istri': default_values['terlalu_tua_istri'],
            'terlalu_dekat_umur': default_values['terlalu_dekat_umur'],
            'terlalu_banyak_anak': default_values['terlalu_banyak_anak']
        }

        # Mengatur flag reset menjadi True setelah reset dilakukan
        st.session_state.reset_flag = True

# Menampilkan hasil prediksi
st.success(f'Hasil Prediksi: {kbst_diagnosis}')

# Menampilkan dataframe hasil prediksi
if input_results:
    st.write('Dataframe Hasil Prediksi:')
    input_results_df = pd.DataFrame(input_results)
    st.write(input_results_df)
    csv = input_results_df.to_csv(index=False)
    st.download_button('Unduh Dataframe Hasil Prediksi', csv, 'predicted_results.csv')
