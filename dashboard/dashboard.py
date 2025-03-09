import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = 'data/merged_df_cleaned.csv'
df = pd.read_csv(file_path)

# Convert date column to datetime
df['datetime'] = pd.to_datetime(df['dteday'])

# Sidebar filters
st.sidebar.header('Filters')
start_date = st.sidebar.date_input('Start Date', df['datetime'].min().date())
end_date = st.sidebar.date_input('End Date', df['datetime'].max().date())
weather_filter = st.sidebar.multiselect('Select Weather Conditions', df['weathersit'].unique(), default=df['weathersit'].unique())

# Apply filters
filtered_df = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date) & (df['weathersit'].isin(weather_filter))]

# Dashboard title
st.title('🚲 Bike Rentals Dashboard')
st.subheader('Analysis of Bike Rental Trends')

# Metrics
total_rentals = filtered_df['cnt_hour'].sum()
avg_temp = filtered_df['temp_hour'].mean()
avg_humidity = filtered_df['hum_hour'].mean()

col1, col2, col3 = st.columns(3)
col1.metric('Total Rentals', f'{total_rentals:,}')
col2.metric('Avg Temperature (°C)', f'{avg_temp:.2f}')
col3.metric('Avg Humidity (%)', f'{avg_humidity:.2f}')

# Visualizations
st.subheader('Bike Rentals Over Time')
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=filtered_df['datetime'], y=filtered_df['cnt_hour'], ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader('Rentals by Day Type')
fig, ax = plt.subplots()
sns.boxplot(x='day_type', y='cnt_hour', data=filtered_df, ax=ax)
st.pyplot(fig)

st.subheader('Seasonal Trends')
fig, ax = plt.subplots()
sns.barplot(x='season', y='cnt_hour', data=filtered_df, estimator=sum, ax=ax)
st.pyplot(fig)

st.subheader('Weather Impact on Rentals')
fig, ax = plt.subplots()
sns.boxplot(x='weathersit', y='cnt_hour', data=filtered_df, ax=ax)
st.pyplot(fig)

# Conclusion
st.header('Insights')
st.write(
    "- **Weekdays vs. Weekends**: Bike usage is higher on weekdays, suggesting commuters use the service for work.\n"
    "- **Seasonal Patterns**: The highest rentals occur in fall, possibly due to pleasant weather.\n"
    "- **Weather Influence**: Clear weather leads to the highest rentals, while rain and snow decrease usage."
)
