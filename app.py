import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

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

# Grafik total suara per kandidat di seluruh kecamatan
if selected_kecamatan == "":
    # Mengumpulkan total suara per kandidat di seluruh kecamatan
    total_candidate_1 = sum([item["totals"]["candidate_1"] for item in data])
    total_candidate_2 = sum([item["totals"]["candidate_2"] for item in data])
    total_candidate_3 = sum([item["totals"]["candidate_3"] for item in data])
    total_candidate_4 = sum([item["totals"]["candidate_4"] for item in data])

    # Membuat DataFrame untuk total suara per kandidat
    totals = pd.DataFrame({
        "Kandidat": ["Kandidat 1", "Kandidat 2", "Kandidat 3", "Kandidat 4"],
        "Jumlah Suara": [total_candidate_1, total_candidate_2, total_candidate_3, total_candidate_4]
    })

    # Visualisasi total suara seluruh kecamatan dengan Line Chart menggunakan Plotly
    st.subheader("Total Suara per Kandidat di Seluruh Kecamatan")
    
    # Membuat line chart untuk total suara per kandidat
    fig = go.Figure()

    # Menambahkan line chart untuk setiap kandidat dengan warna yang berbeda
    fig.add_trace(go.Scatter(
        x=totals["Kandidat"], 
        y=totals["Jumlah Suara"],
        mode='lines+markers',  # garis dan titik
        name="Kandidat 1",
        line=dict(color='blue', width=3),  # Warna biru untuk Kandidat 1
        marker=dict(size=10)
    ))

    fig.add_trace(go.Scatter(
        x=totals["Kandidat"], 
        y=totals["Jumlah Suara"], 
        mode='lines+markers',
        name="Kandidat 2",
        line=dict(color='red', width=3),  # Warna merah untuk Kandidat 2
        marker=dict(size=10)
    ))

    fig.add_trace(go.Scatter(
        x=totals["Kandidat"], 
        y=totals["Jumlah Suara"], 
        mode='lines+markers',
        name="Kandidat 3",
        line=dict(color='green', width=3),  # Warna hijau untuk Kandidat 3
        marker=dict(size=10)
    ))

    fig.add_trace(go.Scatter(
        x=totals["Kandidat"], 
        y=totals["Jumlah Suara"], 
        mode='lines+markers',
        name="Kandidat 4",
        line=dict(color='orange', width=3),  # Warna oranye untuk Kandidat 4
        marker=dict(size=10)
    ))

    fig.update_layout(
        title="Total Suara per Kandidat di Seluruh Kecamatan",
        xaxis_title="Kandidat",
        yaxis_title="Jumlah Suara",
        template="plotly_dark",  # Tema modern dan gelap
        margin=dict(l=100, r=100, t=50, b=50)
    )
    
    st.plotly_chart(fig)

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
    
    # Grafik kecamatan dengan Plotly (Bar Chart)
    fig_kecamatan = go.Figure(data=[
        go.Bar(
            y=totals_kecamatan["Kandidat"], 
            x=totals_kecamatan["Jumlah Suara"],
            orientation="h",
            marker=dict(color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]),
            text=totals_kecamatan["Jumlah Suara"],
            textposition="inside",
            hovertemplate="Kandidat: %{y}<br>Jumlah Suara: %{x}<extra></extra>"
        )
    ])
    
    fig_kecamatan.update_layout(
        title=f"Total Suara - {selected_kecamatan}",
        xaxis_title="Jumlah Suara",
        yaxis_title="Kandidat",
        template="plotly_dark",
        margin=dict(l=100, r=100, t=50, b=50)
    )

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
        fig, ax = plt.subplots()
        kelurahan_df.plot(
            x="TPS",
            y=["Kandidat 1", "Kandidat 2", "Kandidat 3", "Kandidat 4"],
            kind="bar",
            ax=ax
        )
        ax.set_title(f"Suara per TPS di Kelurahan {selected_kelurahan}")
        ax.set_xlabel("TPS")
        ax.set_ylabel("Jumlah Suara")
        st.pyplot(fig)
