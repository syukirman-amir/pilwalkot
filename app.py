import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import plotly.express as px

# Load JSON data
with open('rekapitulasi.json', 'r') as file:
    data = json.load(file)

# Streamlit App
st.title("Rekapitulasi Suara Pilkada")
st.sidebar.title("Navigasi")

# Dropdown untuk memilih kecamatan
kecamatan_list = [item["kecamatan"] for item in data]
selected_kecamatan = st.sidebar.selectbox("Pilih Kecamatan", kecamatan_list)

# Filter data berdasarkan kecamatan yang dipilih
kecamatan_data = next(item for item in data if item["kecamatan"] == selected_kecamatan)

# Tampilkan total suara per kandidat untuk kecamatan
totals = pd.DataFrame(
    kecamatan_data["totals"].items(),
    columns=["Kandidat", "Jumlah Suara"]
)

st.subheader(f"Total Suara - Kecamatan {selected_kecamatan}")
fig = px.bar(totals, x="Kandidat", y="Jumlah Suara", color="Kandidat", title="Total Suara")
st.plotly_chart(fig)

# Dropdown untuk memilih kelurahan
kelurahan_list = list(kecamatan_data["kelurahan"].keys())
selected_kelurahan = st.sidebar.selectbox("Pilih Kelurahan", kelurahan_list)

# Data kelurahan yang dipilih
kelurahan_data = kecamatan_data["kelurahan"][selected_kelurahan]

st.subheader(f"Detail Suara - Kelurahan {selected_kelurahan}")

# Konversi data kelurahan ke DataFrame
kelurahan_df = pd.DataFrame(kelurahan_data)
kelurahan_df = kelurahan_df.rename(columns={
    "candidate_1": "Kandidat 1",
    "candidate_2": "Kandidat 2",
    "candidate_3": "Kandidat 3",
    "candidate_4": "Kandidat 4",
    "tps_number": "TPS"
})

# Tampilkan tabel data
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
