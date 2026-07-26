# Google Play Store Interactive Dashboard

## Project Overview

This project is an interactive dashboard built using Streamlit. The purpose of this project is to make Google Play Store data easier to explore for non-technical users.

Instead of checking the dataset manually, users can select filters and search for applications. The dashboard updates the charts and data table according to the selected options.

## Dataset

For this project, I used a cleaned copy of the Google Play Store dataset.

The dataset contains information about Android applications such as:

- App name
- Category
- Number of reviews
- Number of installs
- App type (Free or Paid)
- Price
- Content rating
- Genres
- Last updated date
- Current version
- Android version

The dataset is included inside this repository so that the project can run independently.

## Interactive Features

The dashboard contains the following interactive controls:

### Category Filter

Users can select a specific app category. The dashboard then shows data related to the selected category.

### App Type Filter

Users can select between Free and Paid applications.

### App Search

Users can search for an application by entering its name. The search is case-insensitive.

### Minimum Installs Filter

Users can enter a minimum number of installs. Only applications with installs equal to or greater than the selected value are displayed.

All these selections update the displayed data and visualizations.

## Visualizations

The dashboard contains three charts:

1. Apps by Category
2. Free vs Paid Apps
3. Top 10 Apps by Installs

These charts are created using the currently filtered dataset. Therefore, the charts change when the user changes the filters.

The dashboard also contains a live data table using `st.dataframe()` which shows the current filtered data.

## External API Integration

I integrated the Open-Meteo weather API into the dashboard using Python's `requests` library.

The API endpoint used is:

https://api.open-meteo.com/v1/forecast

The dashboard sends a GET request to this endpoint.

The API returns weather information in JSON format. From the response, I extract and display the following fields:

- `temperature_2m`
- `wind_speed_10m`

The API call is live, so the weather values are retrieved from the external API when the dashboard runs.

Weather data by Open-Meteo.com (CC BY 4.0).

## Technologies Used

- Python
- Streamlit
- Pandas
- Requests

## Project Structure

```text
Part_3_Dashboard/
│
├── app.py
├── googleplaystore_cleaned.csv
├── requirements.txt
└── README.md