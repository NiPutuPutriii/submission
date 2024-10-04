import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Function to create hourly trends for the year 2011
def create_hourly_trends_2011(df):
    df['dteday'] = pd.to_datetime(df['dteday']) # Convert 'dteday' column to datetime
    hour_df_2011 = df[df['dteday'].dt.year == 2011]
    hour_df_2011['is_weekend'] = hour_df_2011['weekday'].apply(lambda x: 1 if x >= 5 else 0)
    hourly_trends_2011 = hour_df_2011.groupby(['hr', 'is_weekend'])['cnt'].sum().reset_index()
    hourly_trends_2011['is_weekend'] = hourly_trends_2011['is_weekend'].map({0: 'Hari Kerja', 1: 'Akhir Pekan'})    
    return hourly_trends_2011

# Function to create hourly trends for the year 2012
def create_hourly_trends_2012(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    hour_df_2012 = df[df['dteday'].dt.year == 2012]
    hour_df_2012['is_weekend'] = hour_df_2012['weekday'].apply(lambda x: 1 if x >= 5 else 0)
    hourly_trends_2012 = hour_df_2012.groupby(['hr', 'is_weekend'])['cnt'].sum().reset_index()
    hourly_trends_2012['is_weekend'] = hourly_trends_2012['is_weekend'].map({0: 'Hari Kerja', 1: 'Akhir Pekan'})    
    return hourly_trends_2012

# Function to calculate total rentals by weather situation
def create_weather_rentals(df):
    weather_rentals = df.groupby('weathersit')['cnt'].sum()        
    return weather_rentals

# Function to calculate average rentals for casual and registered users by hour
def create_hourly_data(df):
    hourly_data = df.groupby('hr')[['casual', 'registered']].mean()      
    return hourly_data

# Function to calculate total rentals grouped by season and month
def create_season_month_grouped(df):
    season_month_grouped = df.groupby(['season', 'mnth'])['cnt'].sum().reset_index()       
    return season_month_grouped

# Load the dataset from a CSV file
data_df = pd.read_csv("./main_data.csv")

# Create data for each analysis
hourly_trends_2011_data = create_hourly_trends_2011(data_df)
hourly_trends_2012_data = create_hourly_trends_2012(data_df)
weather_rentals_data = create_weather_rentals(data_df)
hourly_data2 = create_hourly_data(data_df)
season_month_grouped_data = create_season_month_grouped(data_df)


# Streamlit app title for hourly bike-sharing trends
st.title('Tren Penggunaan Bike-Sharing Per Jam')

# Plot for 2011 rental trends
st.subheader('Tren Penyewaan (2011)')
fig_2011, ax_2011 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_trends_2011_data, x='hr', y='cnt', hue='is_weekend', marker='o', palette=['#66b3ff','#ff9999'], ax=ax_2011)
ax_2011.set_xlabel('Jam dalam Sehari')
ax_2011.set_ylabel('Total Penyewaan Sepeda')
ax_2011.set_title('Tren Penggunaan Bike-Sharing Per Jam (2011)')
ax_2011.set_xticks(range(0, 24))
ax_2011.legend(title='Jenis Hari')
ax_2011.grid(True)
st.pyplot(fig_2011)

# Plot for 2012 rental trends
st.subheader('Tren Penyewaan (2012)')
fig_2012, ax_2012 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_trends_2012_data, x='hr', y='cnt', hue='is_weekend', marker='o', palette=['#66b3ff','#ff9999'], ax=ax_2012)
ax_2012.set_xlabel('Jam dalam Sehari')
ax_2012.set_ylabel('Total Penyewaan Sepeda')
ax_2012.set_title('Tren Penggunaan Bike-Sharing Per Jam (2011)')
ax_2012.set_xticks(range(0, 24))
ax_2012.legend(title='Jenis Hari')
ax_2012.grid(True)
st.pyplot(fig_2011)


# Create a title for another Streamlit app
st.title('Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan Sepeda')

# Define weather conditions for labeling
weather_labels = ['Cerah/Berawan', 'Berkabut/Mendung', 'Hujan/Sedikit Salju', 'Cuaca Buruk']

# Create a horizontal bar chart using Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(weather_labels, weather_rentals_data.values, color=['#66b3ff', '#99ff99', '#ff9999', '#ffcc99'])

# Add labels and title
ax.set_xlabel('Total Penyewaan Sepeda')
ax.set_title('Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan Sepeda')

# Display the chart in Streamlit
st.pyplot(fig)





# Create a title for another Streamlit app
st.title('Rata-rata Penyewaan Per Jam oleh Pengguna Kasual dan Terdaftar')

# Create a plot for average rentals per hour for casual and registered users
fig, ax = plt.subplots(figsize=(10, 6))

# Plot casual users
ax.plot(hourly_data2.index, hourly_data2['casual'], label='Pengguna Kasual', color='#ff9999', marker='o')

# Plot registered users
ax.plot(hourly_data2.index, hourly_data2['registered'], label='Pengguna Terdaftar', color='#66b3ff', marker='o')

# Add axis labels and title
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_title('Rata-rata Penyewaan Per Jam oleh Pengguna Kasual dan Terdaftar')
ax.legend()

# Show grid and adjust layout
plt.grid(True)
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)


# Create a title for another Streamlit app
st.title('Total Penyewaan Sepeda Berdasarkan Musim dan Bulan')

# Create a bar plot for season and month grouping
plt.figure(figsize=(14, 8))
sns.barplot(data=season_month_grouped_data, x='mnth', y='cnt', hue='season', palette='Set2')
plt.title('Total Penyewaan Sepeda Berdasarkan Musim dan Bulan', fontsize=16)
plt.xlabel('Bulan', fontsize=14)
plt.ylabel('Total Penyewaan', fontsize=14)
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Musim')
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)

