import json
import pandas as pd 
import numpy as np
import streamlit as st

#Geopy's Nominatim
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

@st.cache(allow_output_mutation=True,show_spinner=False)
def select_df_items(appended_df,item):
    #use the item (from item selection) to subset dataframe
    df_temp = appended_df[appended_df["Item Name"]==item].copy()
    return df_temp
    
@st.cache(allow_output_mutation=True,show_spinner=False)
def select_df_points(df_temp,selected):
    #use the points (from map selection) to subset dataframe
    inds = [ x["pointNumber"] for x  in selected if x["curveNumber"]<1]
    df = pd.DataFrame(df_temp[['Hospital Name','Average Charge','lat','lon']].iloc[inds])
    return df
    
@st.cache(allow_output_mutation=True,show_spinner=False)
def load_clean_data(file_name):
    # read in csv into pandas and do some data cleaning and filtering
    appended_df_base = pd.read_csv(file_name)
    appended_df_base.drop("Unnamed: 0", axis=1, inplace=True) # drop index
    df_agg = appended_df_base.groupby(['Item Name','2020 CPT Code'], as_index=False)['Average Charge'].agg(['mean',"std", 'count'])
    agg_2 = df_agg.nlargest(25,'count')
    list_top = [val[0] for val in agg_2.index.values]
    appended_df = appended_df_base[appended_df_base['Item Name'].isin(list_top)] # subset to top 25 most common
    #appended_df[appended_df['Hospital Name'].str.contains("State -")]
    appended_df = appended_df[~appended_df['Hospital Name'].str.contains("State -")]
    return appended_df

@st.cache(show_spinner=False)
def convert_address(address):
	#Here we use Nominatin to convert address to a latitude/longitude coordinates"
	geolocator = Nominatim(user_agent="my_app") #using open street map API 
	Geo_Coordinate = geolocator.geocode(address)
	lat = Geo_Coordinate.latitude
	lon = Geo_Coordinate.longitude
	#Convert the lat long into a list and store as point
	point = [lat, lon]
	return point
    
@st.cache(show_spinner=False)
def quick_stats(df_temp):
    #calc some stats for plotting and display
    val_99 = np.nanpercentile(df_temp["Average Charge"],99)
    val_1 = np.nanpercentile(df_temp["Average Charge"],1)
    val_mean = int(df_temp["Average Charge"].mean())
    val_min = int(df_temp["Average Charge"].min())
    val_max = int(df_temp["Average Charge"].max())   
    return val_1,val_99,val_mean,val_min,val_max

@st.cache(show_spinner=False)
def calc_dist(coord_1, coord_2):
    # distance calculated in mi
    return(great_circle(coord_1, coord_2).mi)