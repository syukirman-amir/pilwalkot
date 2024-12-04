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
    # Menghitung total suara untuk setiap kandidat di seluruh kecamatan
    kandidat_1 = sum([item["totals"]["candidate_1"] for item in data])
    kandidat_2 = sum([item["totals"]["candidate_2"] for item in data])
    kandidat_3 = sum([item["totals"]["candidate_3"] for item in data])
    kandidat_4 = sum([item["totals"]["candidate_4"] for item in data])

    # Membuat DataFrame untuk total suara per kandidat
    totals = pd.DataFrame({
        "Kandidat": ["Kandidat 1", "Kandidat 2", "Kandidat 3", "Kandidat 4"],
        "Jumlah Suara": [kandidat_1, kandidat_2, kandidat_3, kandidat_4]
    })

    # Membuat grafik line dengan 4 garis terpisah, satu untuk tiap kandidat
    fig = px.line(
        totals, 
        x="Kandidat", 
        y="Jumlah Suara", 
        markers=True, 
        title="Total Suara per Kandidat di Seluruh Kecamatan"
    )

    # Menambahkan 4 garis terpisah untuk setiap kandidat
    fig.update_traces(mode='lines+markers')

    # Menampilkan grafik line dengan 4 garis
    st.plotly_chart(fig)

    # Menampilkan grafik batang dengan 4 batang
    fig_bar = px.bar(
        totals, 
        x="Kandidat", 
        y="Jumlah Suara", 
        color="Kandidat", 
        title="Total Suara per Kandidat (Grafik Batang)"
    )
    st.plotly_chart(fig_bar)

else:
    # Setelah memilih kecamatan, tampilkan grafik berdasarkan kecamatan yang dipilih
    kecamatan_data = next(item for item in data if item["kecamatan"] == selected_kecamatan)

    # Tampilkan total suara per kandidat untuk kecamatan yang dipilih
    totals_kecamatan = pd.DataFrame(
        kecamatan_data["totals"].items(),
        columns=["Kandidat", "Jumlah Suara"]
    )

    st.subheader(f"Total Suara - Kecamatan {selected_kecamatan}")
    fig_kecamatan = px.bar(totals_kecamatan, x="Kandidat", y="Jumlah Suara", color="Kandidat", title=f"Total Suara - {selected_kecamatan}")
    st.plotly_chart(fig_kecamatan)

    # Dropdown untuk memilih kelurahan
    kelurahan_list = list(kecamatan_data["kelurahan"].keys())
    selected_kelurahan = st.sidebar.selectbox("Pilih Kelurahan", [""] + kelurahan_list)

    # Setelah memilih kelurahan
    if selected_kelurahan != "":
        # Data kelurahan yang dipilih
        kelurahan_data = kecamatan_data["kelurahan"][selected_kelurahan]

        st.subheader(f"Detail Suara - Kelurahan {selected_kelurahan}")

        # Konversi data kelurahan ke DataFrame
        kelurahan_df = pd.DataFrame(kelurahan_data)

        # Pastikan kolom suara kandidat adalah numerik
        kelurahan_df["candidate_1"] = pd.to_numeric(kelurahan_df["candidate_1"], errors='coerce')
        kelurahan_df["candidate_2"] = pd.to_numeric(kelurahan_df["candidate_2"], errors='coerce')
        kelurahan_df["candidate_3"] = pd.to_numeric(kelurahan_df["candidate_3"], errors='coerce')
        kelurahan_df["candidate_4"] = pd.to_numeric(kelurahan_df["candidate_4"], errors='coerce')

        # Ganti nama kolom untuk memudahkan
        kelurahan_df = kelurahan_df.rename(columns={
            "candidate_1": "Kandidat 1",
            "candidate_2": "Kandidat 2",
            "candidate_3": "Kandidat 3",
            "candidate_4": "Kandidat 4",
            "tps_number": "TPS"
        })

        # Tampilkan tabel data kelurahan
        st.dataframe(kelurahan_df)

        # Plot suara per TPS untuk kelurahan yang dipilih
        fig = px.bar(kelurahan_df, x="TPS", y=["Kandidat 1", "Kandidat 2", "Kandidat 3", "Kandidat 4"],
                     title=f"Suara per TPS di Kelurahan {selected_kelurahan}")
        st.plotly_chart(fig)
