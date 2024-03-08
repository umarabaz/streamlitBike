import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from matplotlib.ticker import FuncFormatter
sns.set(style='dark')

def display_bar_chart(data):
    data['season'] = data['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='cnt', data=data, palette='viridis', ax=ax)

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.0f}'.format(x/1000) + ',000'))

    plt.xlabel('Musim')
    plt.ylabel('Jumlah Penyewaan')

    st.pyplot(fig)

def display_line_chart(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='mnth', y='cnt', data=data, marker='o', color='purple', ax=ax)

    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_xticks(data['mnth'])
    ax.set_xticklabels(data['mnth_label'], rotation=45)

    st.pyplot(fig)

day_df=pd.read_csv("day.csv")

datetime_columns = ["dteday"]
 
for column in datetime_columns:
  day_df[column] = pd.to_datetime(day_df[column])

st.header('Bike Sharing Dashboard')

st.subheader("Jumlah Penyewaan Sepeda berdasarkan Musim")
tabel_penyewaan_musim = day_df.groupby('season')['cnt'].sum().reset_index()
display_bar_chart(tabel_penyewaan_musim)


st.subheader("Jumlah Penyewaan Sepeda berdasarkan bulan dalam 1 tahun terakhir")
tabel_penyewaan_bulanan = day_df[day_df['yr'] == 1].groupby('mnth')['cnt'].sum().reset_index()
nama_bulan = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni',
              7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
tabel_penyewaan_bulanan['mnth_label'] = tabel_penyewaan_bulanan['mnth'].map(nama_bulan)

col1, col2, col3 = st.columns(3)
 
with col1:
    avg_rentals = tabel_penyewaan_bulanan['cnt'].mean()
    st.metric("Rata-rata Penyewaan/Bulan", f"{avg_rentals:.2f}")
 
with col2:
    max_rental_month = tabel_penyewaan_bulanan.loc[tabel_penyewaan_bulanan['cnt'].idxmax(), 'mnth_label']
    st.metric("Bulan Paling Banyak Penyewaan", f"{max_rental_month}")
    

with col3:
    min_rental_month = tabel_penyewaan_bulanan.loc[tabel_penyewaan_bulanan['cnt'].idxmin(), 'mnth_label']
    st.metric("Bulan Paling Sedikit Penyewaan", f"{min_rental_month}")
display_line_chart(tabel_penyewaan_bulanan)

