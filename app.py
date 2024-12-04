import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Load JSON data
with open('rekapitulasi.json', 'r') as file:
    data = json.load(file)

# Streamlit App
st.title("Rekapitulasi Suara Pilwalkot Ternate 2024")

# Bagian untuk memilih kecamatan dan kelurahan untuk melihat detail
st.sidebar.title("iLuv")
kecamatan_list = [item["kecamatan"] for item in data]

# Inisialisasi untuk tidak ada kecamatan dan kelurahan yang dipilih pada awalnya
selected_kecamatan = st.sidebar.selectbox("Pilih Kecamatan", [""] + kecamatan_list)

# Tempat untuk menampilkan grafik total suara seluruh kecamatan
if selected_kecamatan == "":
    # Mengumpulkan data total suara per kandidat per kecamatan
    kecamatan_data = []
    for item in data:
        kecamatan_name = item["kecamatan"]
        total_candidate_1 = item["totals"]["candidate_1"]
        total_candidate_2 = item["totals"]["candidate_2"]
        total_candidate_3 = item["totals"]["candidate_3"]
        total_candidate_4 = item["totals"]["candidate_4"]
        
        # Menyimpan data kecamatan dan total suara untuk setiap kandidat
        kecamatan_data.append({
            "Kecamatan": kecamatan_name,
            "Kandidat 1": total_candidate_1,
            "Kandidat 2": total_candidate_2,
            "Kandidat 3": total_candidate_3,
            "Kandidat 4": total_candidate_4
        })

    # Membuat DataFrame untuk total suara per kecamatan dan per kandidat
    kecamatan_df = pd.DataFrame(kecamatan_data)

    # Mengubah data menjadi format panjang (long format) untuk line chart
    kecamatan_long_df = pd.melt(kecamatan_df, id_vars=["Kecamatan"], value_vars=["Kandidat 1", "Kandidat 2", "Kandidat 3", "Kandidat 4"],
                                var_name="Kandidat", value_name="Jumlah Suara")

    # Visualisasi total suara per kecamatan per kandidat menggunakan Line Chart
    st.subheader("Total Suara per Kecamatan dan Kandidat")
    fig = px.line(kecamatan_long_df, x="Kecamatan", y="Jumlah Suara", color="Kandidat", markers=True, title="Total Suara per Kecamatan dan Kandidat")
    st.plotly_chart(fig, use_container_width=True)

else:
    # Setelah memilih kecamatan, tampilkan grafik berdasarkan kecamatan yang dipilih

    # Filter data berdasarkan kecamatan yang dipilih
    kecamatan_data = next(item for item in data if item["kecamatan"] == selected_kecamatan)

    # Tampilkan total suara per kandidat untuk kecamatan yang dipilih
    totals_kecamatan = pd.DataFrame(
        kecamatan_data["totals"].items(),
        columns=["Kandidat", "Jumlah Suara"]
    )

    st.subheader(f"Total Suara - Kecamatan {selected_kecamatan}")
    fig_kecamatan = px.bar(totals_kecamatan, x="Kandidat", y="Jumlah Suara", color="Kandidat", title=f"Total Suara - {selected_kecamatan}")
    st.plotly_chart(fig_kecamatan, use_container_width=True)

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

        # Pastikan kolom TPS adalah string dengan padding nol
        kelurahan_df["TPS"] = kelurahan_df["TPS"].apply(lambda x: f"{int(x):03d}")  # Pastikan numerik, kemudian format

        # Tampilkan tabel data kelurahan
        with st.expander("Klik untuk melihat detail suara per TPS"):
            st.dataframe(kelurahan_df)

        # Plot suara per TPS untuk kelurahan yang dipilih
        fig = px.bar(kelurahan_df, x="TPS", y=["Kandidat 1", "Kandidat 2", "Kandidat 3", "Kandidat 4"],
                     title=f"Suara per TPS di Kelurahan {selected_kelurahan}")

        # Menyesuaikan label untuk TPS, rotasi agar lebih jelas
        fig.update_layout(
            xaxis_title="TPS",
            yaxis_title="Jumlah Suara",
            xaxis=dict(tickangle=45)  # Mengubah sudut label agar tidak tumpang tindih
        )

        # Menampilkan grafik responsif
        st.plotly_chart(fig, use_container_width=True)
