import streamlit as st
import pandas as pd
import requests

# Load cleaned dataset
df = pd.read_csv("googleplaystore_cleaned.csv")

# Show title
st.title("📱 Google Play Store Dashboard")

# Show dataset information
st.write("Dataset loaded successfully!")

st.write("Shape of dataset:", df.shape)

st.dataframe(df.head())

# Category filter
st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["Category"].dropna().unique().tolist())
)

if selected_category != "All":
    filtered_df = df[df["Category"] == selected_category]
else:
    filtered_df = df

st.subheader("Filtered Dataset")
st.dataframe(filtered_df)
# Dashboard metrics
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Apps", len(filtered_df))

with col2:
    st.metric("Average Reviews", round(filtered_df["Reviews"].mean(), 2))

with col3:
    st.metric("Average Installs", round(filtered_df["Installs"].mean(), 2))
    # Category distribution chart
st.subheader("📱 Apps by Category")

category_counts = filtered_df["Category"].value_counts()

st.bar_chart(category_counts)

# External API Integration
st.subheader(" Live Weather Data")

city = st.selectbox(
    "Select City",
    ["Ahmadnagar", "Mumbai", "Pune", "Delhi", "Bangalore"]
)

city_coordinates = {
    "Ahmadnagar": (19.0952, 74.7496),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Delhi": (28.6139, 77.2090),
    "Bangalore": (12.9716, 77.5946)
}

latitude, longitude = city_coordinates[city]

url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={latitude}&longitude={longitude}"
    f"&current=temperature_2m,wind_speed_10m"
)

response = requests.get(url)

if response.status_code == 200:
    weather_data = response.json()

    temperature = weather_data["current"]["temperature_2m"]
    wind_speed = weather_data["current"]["wind_speed_10m"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(" Temperature", f"{temperature} °C")

    with col2:
        st.metric("Wind Speed", f"{wind_speed} km/h")

else:
    st.error("Unable to fetch weather data.")
    
    
    # App Search
st.sidebar.header("🔍 Search App")

search_app = st.sidebar.text_input(
    "Enter app name"
)

if search_app:
    filtered_df = filtered_df[
        filtered_df["App"].str.contains(
            search_app,
            case=False,
            na=False
        )
    ]
    st.subheader("🔍 Search Results")
st.dataframe(filtered_df)
    
    # Free / Paid Filter
selected_type = st.sidebar.selectbox(
    "Select App Type",
    ["All"] + sorted(df["Type"].dropna().unique().tolist())
)

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["Type"] == selected_type
    ]
    
# Minimum Installs Filter
min_installs = st.sidebar.number_input(
    "Minimum Installs",
    min_value=0,
    value=0,
    step=1000
)

filtered_df = filtered_df[
    filtered_df["Installs"] >= min_installs
]
st.subheader("📱 Apps by Category")

category_counts = filtered_df["Category"].value_counts()

st.bar_chart(category_counts)

st.subheader(" Free vs Paid Apps")

type_counts = filtered_df["Type"].value_counts()

st.bar_chart(type_counts)

st.subheader("📈 Top 10 Apps by Installs")

top_apps = filtered_df.nlargest(
    10,
    "Installs"
)[["App", "Installs"]]

top_apps = top_apps.set_index("App")

st.bar_chart(top_apps)

st.subheader("📋 Filtered App Data")

st.dataframe(filtered_df)

# Live External API Data
st.subheader("🌤️ Live Weather Data")

weather_url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=19.0952"
    "&longitude=74.7496"
    "&current=temperature_2m,wind_speed_10m"
)

response = requests.get(weather_url)

if response.status_code == 200:
    weather_data = response.json()

    current_weather = weather_data["current"]

    temperature = current_weather["temperature_2m"]
    wind_speed = current_weather["wind_speed_10m"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🌡️ Current Temperature",
            f"{temperature} °C"
        )

    with col2:
        st.metric(
            "💨 Wind Speed",
            f"{wind_speed} km/h"
        )

else:
    st.error("Unable to fetch live weather data.")

st.caption("Weather data by Open-Meteo.com (CC BY 4.0)")