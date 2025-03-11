import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("dark")

# Load dataset
day_df = pd.read_csv("data/day_df.csv")

# Konversi kolom date menjadi datetime
day_df['date'] = pd.to_datetime(day_df['date'])

# Konversi 'month' menjadi kategorikal
day_df['month'] = pd.Categorical(day_df['month'], categories=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
], ordered=True)

# Streamlit Layout
st.title("📊 Dashboard Analisis Dataset Bike Sharing")
st.write("Nama : Faturohman Wicaksono")
st.write("Email : faturrohman727@gmail.com")

with st.sidebar:

    # Menambahkan Logo milik saya
    st.image("data/logo.png")

    # Date range filter
    st.sidebar.header("Rentang Waktu")
    min_date = day_df['date'].min()
    max_date = day_df['date'].max()

    start_date = st.sidebar.date_input("Tanggal Mulai", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("Tanggal Akhir", max_date, min_value=min_date, max_value=max_date)

    # Convert date_input to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data by selected date range
    filtered_df = day_df[(day_df['date'] >= start_date) & (day_df['date'] <= end_date)]

    # Sidebar filters for additional interactivity
    st.sidebar.header("Filter Tambahan")
    selected_seasons = st.sidebar.multiselect(
        "Pilih Musim",
        options=day_df['season'].unique(),
        default=day_df['season'].unique()
    )

    selected_weather = st.sidebar.multiselect(
        "Pilih Kondisi Cuaca",
        options=day_df['weather_cond'].unique(),
        default=day_df['weather_cond'].unique()
    )

    # Aplikasikan beberapa filter tambahan
    filtered_df = filtered_df[
        (filtered_df['season'].isin(selected_seasons)) &
        (filtered_df['weather_cond'].isin(selected_weather))
    ]

    # Metrik
    st.sidebar.header("Metrik")
    total_rentals = filtered_df['count'].sum()
    avg_daily_rentals = filtered_df['count'].mean()
    st.sidebar.metric("Total Penyewaan", f"{total_rentals:,.0f}")
    st.sidebar.metric("Rata-rata Penyewaan Harian", f"{avg_daily_rentals:.0f}")

    # Aggregated data
    monthly_counts = filtered_df.groupby("month")["count"].sum().reset_index()
    season_counts = filtered_df.groupby('season')['count'].mean().reset_index()
    pivot_table_day = filtered_df.pivot_table(values="count", index="weekday", columns="weather_cond", aggfunc="mean")


# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Tren Tahunan", "Musim", "Heatmap Cuaca", "Kesimpulan"])

with tab1:
    st.subheader("📈 Tren Penggunaan Sepeda")
    
    # Chart type selector
    chart_type = st.radio("Pilih Jenis Grafik:", ("Line", "Bar"), horizontal=True)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    if chart_type == "Line":
        sns.lineplot(data=monthly_counts, x="month", y="count", marker="o", color="b", ax=ax)
    else:
        sns.barplot(data=monthly_counts, x="month", y="count", color="b", ax=ax)
    
    ax.set_title("Perkembangan Penyewaan Sepeda")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab2:
    st.subheader("🌦️ Penggunaan Sepeda Berdasarkan Musim")
    
    # Color palette selector
    color_palette = st.selectbox("Pilih Palette Warna:", 
                               ("coolwarm", "viridis", "magma", "plasma"))
    
    if not season_counts.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x="season", y="count", data=season_counts, palette=color_palette, ax=ax)
        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Jumlah Penyewa Sepeda")
        st.pyplot(fig)
    else:
        st.warning("Data musim tidak tersedia atau kosong.")

with tab3:
    st.subheader("🔥 Heatmap Penggunaan Sepeda Berdasarkan Hari dan Kondisi Cuaca")
    
    # Heatmap color selector
    heatmap_color = st.selectbox("Pilih Warna Heatmap:", 
                                ("coolwarm", "YlOrRd", "viridis", "magma"))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(pivot_table_day, cmap=heatmap_color, annot=True, fmt=".1f", linewidths=0.3, ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Hari dalam Seminggu")
    st.pyplot(fig)

with tab4:
    st.subheader("📌 Kesimpulan")
    st.markdown("""
    **1️⃣ Pola Penggunaan Sepeda dalam Setahun:**
    - Penggunaan sepeda meningkat dari awal tahun hingga musim panas.
    - Puncak penggunaan terjadi di pertengahan tahun (Juni - September).
    - Setelah bulan September, penggunaan menurun hingga akhir tahun.
    
    **2️⃣ Musim dengan Penggunaan Tertinggi:**
    - Musim gugur (Fall) memiliki penggunaan tertinggi.
    - Musim semi (Spring) memiliki penggunaan terendah.
    
    **3️⃣ Pengaruh Cuaca terhadap Penggunaan Sepeda:**
    - Kondisi cuaca yang lebih baik berkontribusi pada peningkatan jumlah penyewa.
    - Cuaca buruk seperti hujan atau salju cenderung menurunkan jumlah pengguna sepeda.
    """)

st.write("Dashboard ini memberikan gambaran lengkap mengenai pola penggunaan sepeda berdasarkan waktu dan kondisi cuaca. 🚴‍♂️📊")
