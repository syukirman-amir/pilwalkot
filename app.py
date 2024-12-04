import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Load JSON data
with open('rekapitulasi.json', 'r') as file:
    data = json.load(file)

# Streamlit App
st.title("Rekapitulasi Suara Pilkada")

# Tampilkan total suara seluruh kecamatan per kandidat

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

# Visualisasi total suara seluruh kecamatan
st.subheader("Total Suara per Kandidat di Seluruh Kecamatan")
fig = px.bar(totals, x="Kandidat", y="Jumlah Suara", color="Kandidat", title="Total Suara per Kandidat")
st.plotly_chart(fig)

# Bagian untuk memilih kecamatan dan kelurahan untuk melihat detail
st.sidebar.title("Navigasi")
kecamatan_list = [item["kecamatan"] for item in data]
selected_kecamatan = st.sidebar.selectbox("Pilih Kecamatan", kecamatan_list)

# Filter data berdasarkan kecamatan yang dipilih
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
selected_kelurahan = st.sidebar.selectbox("Pilih Kelurahan", kelurahan_list)

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
