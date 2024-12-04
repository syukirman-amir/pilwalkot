import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# Load JSON data
with open('rekapitulasi.json', 'r') as file:
    data = json.load(file)

# Sample data for coordinates of kecamatan (You need to replace this with real coordinates)
kecamatan_coordinates = {
    "Nama Kecamatan": {"lat": -6.1751, "lon": 106.8650},  # Replace with actual coordinates
    # Add more kecamatan with latitudes and longitudes
}

# Streamlit App
st.title("Rekapitulasi Suara Pilkada")
st.sidebar.title("Navigasi")

# Dropdown untuk memilih kecamatan
kecamatan_list = [item["kecamatan"] for item in data]
selected_kecamatan = st.sidebar.selectbox("Pilih Kecamatan", kecamatan_list)

# Filter data berdasarkan kecamatan yang dipilih
kecamatan_data = next(item for item in data if item["kecamatan"] == selected_kecamatan)

# Visualisasi Peta Total Suara per Kecamatan
st.subheader("Peta Suara per Kecamatan")

# Siapkan data untuk peta choropleth
kecamatan_names = []
candidate_1_votes = []
candidate_2_votes = []
candidate_3_votes = []
candidate_4_votes = []
latitudes = []
longitudes = []

for kecamatan in data:
    kecamatan_names.append(kecamatan["kecamatan"])
    candidate_1_votes.append(kecamatan["totals"]["candidate_1"])
    candidate_2_votes.append(kecamatan["totals"]["candidate_2"])
    candidate_3_votes.append(kecamatan["totals"]["candidate_3"])
    candidate_4_votes.append(kecamatan["totals"]["candidate_4"])
    latitudes.append(kecamatan_coordinates.get(kecamatan["kecamatan"], {}).get("lat", 0))
    longitudes.append(kecamatan_coordinates.get(kecamatan["kecamatan"], {}).get("lon", 0))

# Buat dataframe untuk peta
df_map = pd.DataFrame({
    'Kecamatan': kecamatan_names,
    'Candidate 1': candidate_1_votes,
    'Candidate 2': candidate_2_votes,
    'Candidate 3': candidate_3_votes,
    'Candidate 4': candidate_4_votes,
    'Latitude': latitudes,
    'Longitude': longitudes
})

# Plot peta dengan Plotly
fig_map = px.scatter_geo(df_map, lat="Latitude", lon="Longitude", text="Kecamatan",
                         size="Candidate 1", color="Candidate 1",
                         hover_name="Kecamatan", title="Peta Total Suara per Kecamatan")
st.plotly_chart(fig_map)

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
