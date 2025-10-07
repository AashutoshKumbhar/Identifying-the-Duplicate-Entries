import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


df = pd.read_excel("customer_data_real_addresses.xlsx")


df["Full_Address"] = df["Address1"] + ", " + df["Address2"] + ", " + df["Address3"]

#Convert address to coordinates
geolocator = Nominatim(user_agent="geo_deduplication")

def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except:
        return None, None
    return None, None

df["Latitude"], df["Longitude"] = zip(*df["Full_Address"].apply(get_coordinates))

#Identify duplicates using coordinates
unique_customers = {}

for _, row in df.iterrows():
    key = (row["Name"], row["Department"])  # Unique identifier for a person
    lat, lon = row["Latitude"], row["Longitude"]

    if key in unique_customers:
        existing = unique_customers[key]
        existing_lat, existing_lon = existing["Latitude"], existing["Longitude"]

        # Check if coordinates are very close (within 50 meters)
        if geodesic((lat, lon), (existing_lat, existing_lon)).meters < 50:
            # Merge addresses
            existing["Full_Address"] = ', '.join(set([existing["Full_Address"], row["Full_Address"]]))
        else:
            unique_customers[key + (lat, lon)] = row  # Treat as a separate entry

    else:
        unique_customers[key] = row  # Add as a new unique customer


df_cleaned = pd.DataFrame(unique_customers.values())
df_cleaned

df_final = df_cleaned.sort_values(by="Name")
df_final
df_final.to_excel("cleaned_customer_data.xlsx")