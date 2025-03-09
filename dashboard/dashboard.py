import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

# Load dataset
file_path = 'data/merged_df_cleaned.csv'
df = pd.read_csv(file_path)

df['dteday'] = pd.to_datetime(df['dteday'])

# Sidebar Filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df['dteday'].min())
end_date = st.sidebar.date_input("End Date", df['dteday'].max())
weather_options = df['weathersit'].unique().tolist()
selected_weather = st.sidebar.multiselect("Select Weather Conditions", weather_options, default=weather_options)

# Ensure at least one weather condition is selected
if not selected_weather:
    st.sidebar.error("Please select at least one weather condition.")
    st.stop()

filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date)) & (df['weathersit'].isin(selected_weather))]

# Main Dashboard Title
st.title("🚲 Bike Rentals Dashboard")
st.write("Name : Faturohman Wicaksono")
st.write("Email : faturrohman727@gmail.com")
# Tabs for Overview, Visualization, Clustering & Conclusion
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Visualization", "Clustering", "Conclusion"])

with tab1:
    st.header("🎯 Dashboard Purpose")
    st.markdown(
        """
        This dashboard aims to answer three key business questions regarding bike rental usage:
        
        1. **Is bike usage higher on weekdays compared to weekends?**
        2. **What are the seasonal patterns of bike rentals? Is there a peak season?**
        3. **How can we predict bike rental numbers based on weather and time factors?**
        """
    )
    
    st.header("📌 About")
    st.markdown(
        """
        The bike-sharing rental process is highly correlated to environmental and seasonal factors. For example, weather conditions, precipitation, day of the week, season, and time of day can influence rental behaviors. The core dataset includes two years of historical data from the Capital Bikeshare system in Washington, D.C., USA, covering the years 2011 and 2012, which is publicly available at Capital Bikeshare Data.

        The data has been aggregated on an hourly and daily basis, with additional weather and seasonal information added. Weather information is sourced from Free Meteo.
        """
    )
    
    st.header("🔗 Source")
    st.markdown("[Dataset Source](https://www.kaggle.com/c/bike-sharing-demand/data)")

with tab2:
    st.header("📊 Data Visualization")
    
    # User Count per Day Type
    st.subheader("Bike Rentals on Workdays vs Weekends")
    if not filtered_df.empty:
        day_type_counts = filtered_df.groupby("day_type")["cnt_hour"].sum()
        fig, ax = plt.subplots()
        day_type_counts.plot(kind='bar', ax=ax, color=['blue', 'orange'])
        plt.xticks(rotation=0)
        plt.ylabel("Total Rentals")
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")
    
    # Seasonal Usage Pattern
    st.subheader("Bike Rentals Across Seasons")
    if not filtered_df.empty:
        season_counts = filtered_df.groupby("season")["cnt_hour"].sum()
        fig, ax = plt.subplots()
        season_counts.plot(kind='bar', ax=ax, color=['green', 'red', 'blue', 'purple'])
        plt.xticks(rotation=0)
        plt.ylabel("Total Rentals")
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")
    
    # Weather Impact on Bike Rentals
    st.subheader("Impact of Weather on Bike Rentals")
    if not filtered_df.empty:
        weather_counts = filtered_df.groupby("weathersit")["cnt_hour"].sum()
        fig, ax = plt.subplots()
        weather_counts.plot(kind='bar', ax=ax, color=['gray', 'yellow', 'blue'])
        plt.xticks(rotation=0)
        plt.ylabel("Total Rentals")
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")

with tab3:
    st.header("🔍 Clustering Analysis: User Rental Intensity")
    
    if not filtered_df.empty:
        # Binning users into clusters based on rental counts
        filtered_df['rental_cluster'] = pd.qcut(filtered_df['cnt_hour'], q=3, labels=["Low", "Medium", "High"])
        cluster_counts = filtered_df['rental_cluster'].value_counts()
        
        st.subheader("User Rental Clusters")
        fig, ax = plt.subplots()
        cluster_counts.plot(kind='bar', ax=ax, color=['blue', 'orange', 'red'])
        plt.xticks(rotation=0)
        plt.ylabel("Number of Days")
        st.pyplot(fig)
        
        st.markdown(
            """
            ### Interpretation:
            - **Low Usage:** Days with the lowest rental activity.
            - **Medium Usage:** Moderate rental activity.
            - **High Usage:** Peak rental days, often correlating with good weather and workdays.
            """
        )
    else:
        st.warning("No data available for the selected filters.")

with tab4:
    st.header("📌 Conclusion")
    st.markdown(
        """
        - **Weekday vs Weekend:** Bike rentals are generally higher on workdays compared to weekends.
        - **Seasonal Trends:** Fall season shows the highest bike rental activity, possibly due to favorable weather conditions.
        - **Weather Impact:** Clear weather leads to higher bike rentals, while bad weather (rain/snow) significantly reduces usage.
        - **Peak Hours:** Rentals peak during commuting hours (morning and evening), showing dependency on work-related usage.
        - **Clustering Insight:** High rental days occur mostly on workdays with good weather, while low rental days correspond to weekends or bad weather days.
        """
    )
