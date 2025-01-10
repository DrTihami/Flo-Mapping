import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# Load the data
flo_data = pd.read_csv('FLO_Mapped_df')

# Check if the necessary columns exist
if 'Flo_Latitude' in flo_data.columns and 'Flo_Longitude' in flo_data.columns:
    # Convert FLO coordinates into a numpy array for BallTree
    flo_coords = flo_data[['Flo_Latitude', 'Flo_Longitude']].values
    ball_tree = BallTree(np.radians(flo_coords), metric='haversine')

    # Streamlit UI
    st.title("Farmer to Nearest FLO Locator")

    # Get farmer location from user
    farmer_lat = st.number_input("Enter Farmer Latitude", min_value=33.00000, max_value=36.00000, value=33.5)
    farmer_lon = st.number_input("Enter Farmer Longitude", min_value=73.50000, max_value=76.00000, value=75.0)

    # Query BallTree to find the nearest FLO
    farmer_coords = np.array([[farmer_lat, farmer_lon]])
    distances, indices = ball_tree.query(np.radians(farmer_coords), k=1)

    # Display the nearest FLO details
    nearest_flo_idx = indices[0][0]
    nearest_flo = flo_data.iloc[nearest_flo_idx]
    st.write(f"Nearest FLO to Farmer at ({farmer_lat}, {farmer_lon}):")
    st.write(f"**FLO Name**: {nearest_flo['Flo_Name']}")
    st.write(f"**FLO Address **: {nearest_flo['Flo_Address']}")
    st.write(f"**FLO District**: {nearest_flo['Flo_District']}")
    st.write(f"**Distance**: {distances[0][0] * 6371:.2f} km")
else:
    st.error("The dataset does not contain the required 'Flo_Latitude' and 'Flo_Longitude' columns.")