import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree  # Correct import from scikit-learn

# Load the data
flo_data = pd.read_csv('FLO_Mapped_df.csv')  # Make sure the file name includes '.csv'

# Function to find the nearest FLO
def Assign_Nearest_Flo(lat, lon, data, ball_tree):
    farmer_coords = np.array([[lat, lon]])
    distances, indices = ball_tree.query(np.radians(farmer_coords), k=1)
    nearest_flo_idx = indices[0][0]
    nearest_flo = data.iloc[nearest_flo_idx]
    distance_km = distances[0][0] * 6371  # Convert distance from radians to kilometers
    return nearest_flo, distance_km

# Check if the necessary columns exist
if 'Flo_Latitude' in flo_data.columns and 'Flo_Longitude' in flo_data.columns:
    # Convert FLO coordinates into a numpy array for BallTree
    flo_coords = flo_data[['Flo_Latitude', 'Flo_Longitude']].values
    ball_tree = BallTree(np.radians(flo_coords), metric='haversine')

    # Streamlit UI
    # Title with blue box
    st.markdown(
        """
        <div style="background-color: #007BFF; padding: 10px; border-radius: 5px;">
            <h1 style="color: white; text-align: center;">Nearest FLO Locator</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Subheading with smaller font size
    st.markdown(
        """
        <div style="background-color: #E6F7FF; padding: 10px; border-radius: 5px; margin-top: 10px;">
            <h3 style="color: #004085; text-align: center; font-size: 18px;">
                Objective of Application: This application helps find the nearest Field Level Officer for farmers based on their latitude and longitude coordinates. JKVDA Kashmir Courtesy.
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Get farmer location from user
    farmer_lat = st.number_input(
        "Enter Farmer Latitude",
        min_value=33.00000,
        max_value=35.00000,
        value=33.99039,
        format="%.5f"
    )
    farmer_lon = st.number_input(
        "Enter Farmer Longitude",
        min_value=73.50000,
        max_value=75.50000,
        value=74.87782,
        format="%.5f"
    )

    # Button to assign nearest FLO
    if st.button("Assign Nearest_Flo"):
        nearest_flo, distance_km = Assign_Nearest_Flo(farmer_lat, farmer_lon, flo_data, ball_tree)

        # Display the output
        st.write(f"Nearest FLO to Farmer at ({farmer_lat}, {farmer_lon}):")
        st.write(f"**FLO Name**: {nearest_flo['Flo_Name of the Centre']}")
        st.write(f"**FLO Address**: {nearest_flo['Flo_Address']}")
        st.write(f"**FLO District**: {nearest_flo['Flo_District']}")
        st.write(f"**Distance**: {distance_km:.2f} km")
else:
    st.error("The dataset does not contain the required 'Flo_Latitude' and 'Flo_Longitude' columns.")
