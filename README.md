# Bike Rentals Dashboard

## 📌 Overview
This dashboard provides insights into bike rental trends using historical data. It helps businesses optimize resources and improve service availability. The dashboard aims to answer the following key business questions:

1. **Is bike usage higher on weekdays compared to weekends?**
2. **What are the seasonal patterns of bike rentals? Is there a peak season?**
3. **How can we predict bike rental numbers based on weather and time factors?**

## 🚀 Features
- **Date & Weather Filters**: Users can filter data by date range and weather conditions (at least one must be selected).
- **Data Visualizations**: Various charts to analyze bike rental patterns based on weekdays, seasons, and weather impact.
- **Clustering Analysis**: Groups rental intensity into three categories (Low, Medium, High) to identify patterns.
- **Conclusion Section**: Summarizes key findings from the data analysis.
- **About & Source Information**: Provides details about the dataset and the purpose of the dashboard.

## 📊 Tabs
### **1. Overview**
- Dashboard purpose
- About section
- Dataset source ([Bike Sharing Dataset](https://www.kaggle.com/c/bike-sharing-demand/data))

### **2. Visualization**
- **Weekday vs Weekend Rentals**: Bar chart comparing bike rentals on workdays and weekends.
- **Seasonal Rental Trends**: Analyzes bike rentals across different seasons.
- **Weather Impact on Rentals**: Explores how weather conditions affect bike rental activity.

### **3. Clustering**
- Groups bike rental data into three categories: **Low**, **Medium**, and **High** usage days.
- Helps identify patterns related to rental demand intensity.

### **4. Conclusion**
- Summary of key findings from the data.
- Insights into how bike rentals vary based on time, weather, and seasons.

## 🛠️ Technologies Used
- **Python** (Pandas, Matplotlib, Seaborn, NumPy)
- **Streamlit** (for building the interactive dashboard)

## 🔧 How to Run the Application

1. **Requirements**
   - Python 3.10 or later.
   - Streamlit and other required libraries.
   
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run dashboard.py
   ```

4. **Access the Dashboard**
   Once the command is executed, open your browser and visit **http://localhost:8501/** or go to [here](https://faturohmanw23.streamlit.app/).

## 🎯 Key Insights
- **Workday rentals** are generally **higher** than weekend rentals.
- **Fall season** has the highest rental activity, possibly due to favorable weather.
- **Clear weather** leads to **higher rentals**, while bad weather (rain/snow) reduces usage.
- **Peak rental hours** are during commuting times (morning & evening).

This dashboard is designed to help businesses and policymakers make data-driven decisions regarding bike rental services.

