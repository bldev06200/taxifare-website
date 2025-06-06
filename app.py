import streamlit as st
import requests as requests
from PIL import Image
import numpy as np
import urllib.request
import matplotlib.pyplot as plt

st.title("TaxiFareModel front")

st.header("Please chose your parameters")

pickup_date = st.date_input("Ride date",)
pickup_time = st.time_input("Ride time",)
pickup_longitude = st.number_input("Pickup longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup latitude", value=40.748817)
dropoff_longitude = st.number_input("Drop-off longitude", value=-73.985428)
dropoff_latitude = st.number_input("Drop-off latitude", value=-40.748817)
passenger_count = st.slider("passenger count", 1,8,1)

# Once we have these, let's call our API in order to retrieve a prediction
#See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...
#🤔 How could we call our API ? Off course... The `requests` package 💡


url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    #2. Let's build a dictionary containing the parameters for our API...
    

    pickup_datetime = f"{pickup_date} {pickup_time}"
    param_dict = {"pickup_datetime": pickup_datetime,
                "pickup_longitude": pickup_longitude,
                "pickup_latitude": pickup_latitude,
                "dropoff_longitude": dropoff_longitude,
                "dropoff_latitude": dropoff_latitude,
                "passenger_count": passenger_count
    }

    #3. Let's call our API using the `requests` package...
    

if st.button("Get predictions ! "):
    response = requests.get(url, params=param_dict)


    #4. Let's retrieve the prediction from the **JSON** returned by the API...


    if response.status_code == 200:
        prediction = response.json()["fare"]
    else: 
        st.error("Failed at predicting the price")

    # Finally, we can display the prediction to the user


    st.success(f"Our prediction is {prediction:.2f} $$ for going from here: ")

    url = 'https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/nyc_-74.3_-73.7_40.5_40.9.png'
    nyc_map = np.array(Image.open(urllib.request.urlopen(url)))
    def plot_on_map(longitude, latitude, BB, nyc_map, s=10, alpha=0.2):
        fig, axs = plt.subplots(figsize=(16,10))

        axs.scatter(longitude, latitude, zorder=1, alpha=alpha, c='red', s=s,marker='x')
        axs.set_xlim((BB[0], BB[1]))
        axs.set_ylim((BB[2], BB[3]))
        axs.set_title('locations')
        axs.imshow(nyc_map, zorder=0, extent=BB)
        st.pyplot(fig)
        
    BB = (-74.3, -73.7, 40.5, 40.9)

    plot_on_map(param_dict["pickup_longitude"], param_dict["pickup_latitude"], BB, nyc_map, s=80, alpha=1)

    st.write("to here!")
    plot_on_map(param_dict["dropoff_longitude"], param_dict["dropoff_latitude"], BB, nyc_map, s=80, alpha=1)
