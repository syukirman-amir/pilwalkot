import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import plotly.express as px

# Load JSON data
with open('rekapitulasi_suara.json', 'r') as file:
    data = json.load(file)

# Streamlit App
st.title("Rekapitulasi Suara Pilkada")
st.sidebar.title("Pilih Kecamatan")
kecamatan_list = [item["kecamatan"] for item in data]

# Dropdown untuk memilih kecamatan
selected_kecamatan = st.sidebar.selectbox("Kecamatan", kecamatan_list)

# Filter data berdasarkan kecamatan yang dipilih
kecamatan_data = next(item for item in data if item["kecamatan"] == selected_kecamatan)

# Tampilkan total suara per kandidat
totals = pd.DataFrame(
    kecamatan_data["totals"].items(),
    columns=["Kandidat", "Jumlah Suara"]
)

st.subheader(f"Total Suara - {selected_kecamatan}")
fig = px.bar(totals, x="Kandidat", y="Jumlah Suara", color="Kandidat", title="Total Suara")
st.plotly_chart(fig)

# Visualisasi per kelurahan
st.subheader(f"Detail Suara per Kelurahan - {selected_kecamatan}")

for kelurahan, tps_data in kecamatan_data["kelurahan"].items():
    st.write(f"### Kelurahan: {kelurahan}")
    
    # Konversi TPS data menjadi DataFrame
    kelurahan_df = pd.DataFrame(tps_data)
    st.dataframe(kelurahan_df)
    
    # Plot suara per TPS
    fig, ax = plt.subplots()
    kelurahan_df.plot(
        x="tps_number",
        y=["candidate_1", "candidate_2", "candidate_3", "candidate_4"],
        kind="bar",
        ax=ax
    )
    ax.set_title(f"Suara per TPS di Kelurahan {kelurahan}")
    ax.set_xlabel("TPS")
    ax.set_ylabel("Jumlah Suara")
    st.pyplot(fig)
