import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Setting Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# 2. Load Data (Path otomatis biar gak error)
@st.cache_data
def load_data():
    basepath = os.path.dirname(__file__)
    # Membaca dua file sesuai kebutuhan kode Claude
    day = pd.read_csv(os.path.join(basepath, 'main_data.csv'))
    hour = pd.read_csv(os.path.join(basepath, 'hour_data.csv'))
    
    day['dteday'] = pd.to_datetime(day['dteday'])
    hour['dteday'] = pd.to_datetime(hour['dteday'])
    return day, hour

day_df, hour_df = load_data()

# 3. Sidebar (Filter)
st.sidebar.title("🚲 Bike Sharing")
year_filter = st.sidebar.multiselect("Tahun:", [2011, 2012], default=[2011, 2012])
season_filter = st.sidebar.multiselect("Musim:", ['Spring', 'Summer', 'Fall', 'Winter'], 
                                       default=['Spring', 'Summer', 'Fall', 'Winter'])

# Terapkan Filter
df_day = day_df[(day_df['year'].isin(year_filter)) & (day_df['season_label'].isin(season_filter))]
df_hour = hour_df[(hour_df['year'].isin(year_filter)) & (hour_df['season_label'].isin(season_filter))]

# 4. Header & Ringkasan
st.title("🚲 Dashboard Analisis Bike Sharing")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Pinjam", f"{df_day['cnt'].sum():,}")
c2.metric("Rata-rata/Hari", f"{df_day['cnt'].mean():,.0f}")
c3.metric("User Casual", f"{df_day['casual'].sum():,}")
c4.metric("User Registered", f"{df_day['registered'].sum():,}")

st.divider()

# 5. Tab Layout (Sesuai permintaan)
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tren", "🌤️ Cuaca", "⏰ Jam", "🔵 Segmen"])

# --- TAB 1: Tren Bulanan ---
with tab1:
    st.subheader("Bagaimana Tren Peminjaman per Bulan dan Musim?")
    monthly = df_day.resample('ME', on='dteday').agg({'cnt':'sum', 'registered':'sum', 'casual':'sum'}).reset_index()
    monthly['month_name'] = monthly['dteday'].dt.strftime('%Y-%m')
    
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    # Kiri: Line Chart
    ax[0].plot(monthly['month_name'], monthly['cnt'], marker='o', label='Total', color='#2196F3')
    ax[0].plot(monthly['month_name'], monthly['registered'], ls='--', label='Registered', color='#4CAF50')
    ax[0].plot(monthly['month_name'], monthly['casual'], ls='--', label='Casual', color='#FF9800')
    ax[0].set_title("Tren Bulanan")
    ax[0].tick_params(axis='x', rotation=45)
    ax[0].legend()
    
    # Kanan: Bar Musim
    colors = {'Spring': '#4CAF50', 'Summer': '#FF9800', 'Fall': '#F44336', 'Winter': '#2196F3'}
    sns.barplot(x='season_label', y='cnt', data=df_day, palette=colors, ax=ax[1])
    ax[1].set_title("Rata-rata per Musim")
    st.pyplot(fig)

# --- TAB 2: Cuaca ---
with tab2:
    st.subheader("Pengaruh Cuaca dan Suhu")
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(x='weather_label', y='cnt', data=df_day, ax=ax[0])
    sns.scatterplot(x='temp_celsius', y='cnt', hue='season_label', data=df_day, ax=ax[1])
    st.pyplot(fig)

# --- TAB 3: Jam ---
with tab3:
    st.subheader("Pola Peminjaman Per Jam")
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    # Line chart jam
    workday = df_hour[df_hour['workingday']==1].groupby('hr')['cnt'].mean()
    weekend = df_hour[df_hour['workingday']==0].groupby('hr')['cnt'].mean()
    ax[0].plot(workday, label='Hari Kerja', color='#1565C0')
    ax[0].plot(weekend, label='Libur', ls='--', color='#FF7043')
    ax[0].legend()
    
    # Heatmap
    pivot = df_hour.pivot_table(index='weekday', columns='hr', values='cnt', aggfunc='mean')
    sns.heatmap(pivot, cmap='YlOrRd', ax=ax[1])
    st.pyplot(fig)

# --- TAB 4: Segmentasi (Manual Clustering) ---
with tab4:
    st.subheader("Segmentasi Demand (Clustering Manual)")
    
    # Perhitungan Quantile (Rumus Tetap Sama)
    q1, q2 = df_day['cnt'].quantile(0.33), df_day['cnt'].quantile(0.66)
    
    def make_segmen(x):
        if x <= q1: return 'Low Demand'
        if x <= q2: return 'Medium Demand'
        return 'High Demand'
    
    df_day['segment'] = df_day['cnt'].apply(make_segmen)
    
    # 1. Tampilkan Tabel Statistik (Seperti di gambar kamu)
    st.write("Statistik Deskriptif per Segmen:")
    st.dataframe(df_day.groupby('segment')['cnt'].describe().round(2), use_container_width=True)
    
    # 2. Membuat 3 Grafik dalam satu baris
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # --- Grafik 1: Pie Chart (Proporsi Hari) ---
    seg_counts = df_day['segment'].value_counts().reindex(['Low Demand', 'Medium Demand', 'High Demand'])
    axes[0].pie(seg_counts, labels=seg_counts.index, autopct='%1.1f%%', 
                colors=['#EF5350', '#FFA726', '#66BB6A'], startangle=90)
    axes[0].set_title("Proporsi Hari per Segmen")
    
    # --- Grafik 2: Bar Chart (Casual vs Registered) ---
    seg_users = df_day.groupby('segment')[['casual', 'registered']].mean().reindex(['Low Demand', 'Medium Demand', 'High Demand'])
    seg_users.plot(kind='bar', ax=axes[1], color=['#FF9800', '#2196F3'])
    axes[1].set_title("Rata-rata User per Segmen")
    axes[1].set_xticklabels(['Low', 'Med', 'High'], rotation=0)
    
    # --- Grafik 3: Boxplot (Suhu) ---
    sns.boxplot(x='segment', y='temp_celsius', data=df_day, 
                order=['Low Demand', 'Medium Demand', 'High Demand'], 
                palette=['#EF5350', '#FFA726', '#66BB6A'], ax=axes[2])
    axes[2].set_title("Distribusi Suhu per Segmen")
    
    plt.tight_layout()
    st.pyplot(fig)

st.caption("Copyright © 2026 - Harnum Adinda Putri")