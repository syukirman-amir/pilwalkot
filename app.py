import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Load JSON data
with open('rekapitulasi.json', 'r') as file:
    data = json.load(file)

# Streamlit App
st.title("Rekapitulasi Suara Pilkada")

# Bagian untuk memilih kecamatan dan kelurahan untuk melihat detail
st.sidebar.title("Navigasi")
kecamatan_list = [item["kecamatan"] for item in data]

# Inisialisasi untuk tidak ada kecamatan dan kelurahan yang dipilih pada awalnya
selected_kecamatan = st.sidebar.selectbox("Pilih Kecamatan", [""] + kecamatan_list)

# Tempat untuk menampilkan grafik total suara seluruh kecamatan
if selected_kecamatan == "":
    # Mengumpulkan total suara per kandidat di seluruh kecamatan
    total_candidate_1 = sum([item["totals"]["candidate_1"] for item in data])
    total_candidate_2 = sum([item["totals"]["candidate_2"] for item in data])
    total_candidate_3 = sum([item["totals"]["candidate_3"] for item in data])
    total_candidate_4 = sum([item["totals"]["candidate_4"] for item in data])

    # Membuat DataFrame untuk total suara per kandidat
    totals = pd.DataFrame({
        "Kandidat 1": [total_candidate_1],
        "Kandidat 2": [total_candidate_2],
        "Kandidat 3": [total_candidate_3],
        "Kandidat 4": [total_candidate_4]
    })

    # Menampilkan grafik Line Chart dengan 4 garis untuk setiap kandidat
    st.subheader("Total Suara per Kandidat di Seluruh Kecamatan")
    st.line_chart(totals.T)  # .T untuk transpose agar setiap kandidat menjadi satu garis

else:
    # Setelah memilih kecamatan, tampilkan grafik berdasarkan kecamatan yang dipilih
    kecamatan_data = next(item for item in data if item["kecamatan"] == selected_kecamatan)

    # Tampilkan total suara per kandidat untuk kecamatan yang dipilih
    totals_kecamatan = pd.DataFrame(
        kecamatan_data["totals"].items(),
        columns=["Kandidat", "Jumlah Suara"]
    )

    st.subheader(f"Total Suara - Kecamatan {selected_kecamatan}")
    st.line_chart(totals_kecamatan.set_index("Kandidat").T)  # .T untuk transpose agar setiap kandidat menjadi satu garis
