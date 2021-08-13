import streamlit as st
from streamlit_plotly_events import plotly_events
#Import plotly express and plotly graph_objects
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 
import numpy as np
import os

st.set_page_config(page_title='Hospital Cost Finder', page_icon="https://api.iconify.design/ic:baseline-local-hospital.svg?color=orange") # background: url('https://api.iconify.design/openmoji:hospital.svg') no-repeat center center / contain;

from helpers import select_df_items,select_df_points,convert_address,load_clean_data,quick_stats
from plotting_helpers import create_map,make_state_violin,make_combined_violin,make_table,create_map_base,map_location

token = os.environ['TOKEN']

appended_df = load_clean_data('Charge_data_2.csv')

st.title('Sir Charge A Lot')

st.header('Find and compare hospital costs in California')

address = st.text_input("Enter a location:  ", "San Francisco, CA")

new_row = {'Item Name':'', 'lat':0, 'lon':0, 'Average Charge':0}

appended_df = appended_df.append(new_row, ignore_index=True)

item_select = st.selectbox('Select a service:',sorted(appended_df['Item Name'].unique()))

cpt_pick = appended_df["2020 CPT Code"][appended_df['Item Name']==item_select].unique()

df_temp = select_df_items(appended_df,item_select)

if address:
    coordinates = convert_address(address)
    zoom_val = 10

map1 = st.empty()

if len(df_temp)==1:
    fig = create_map_base(appended_df,coordinates,zoom_val,token)
    fig = map_location(fig,coordinates)
    map1.plotly_chart(fig, use_container_width=True)
    
if item_select:
    map1.empty()
    
    if len(df_temp)>1:
        val_1,val_99,val_mean,val_min,val_max = quick_stats(df_temp)
        st.subheader('State average = $' + str(val_mean) + '. State range = $' + str(val_min) + ' - $' +  str(val_max)   )
        fig = create_map(df_temp,coordinates,zoom_val,val_1,val_99,token)
        selected_points = plotly_events(fig, click_event=True,select_event=True,override_width='95%')

        my_expander_dist  = st.beta_expander(label='See Data Distribution: ')

        with my_expander_dist:
            point_vis = 'suspectedoutliers'  
            var1 = st.empty()
            fig_dist = make_state_violin(df_temp,point_vis)
            var1.plotly_chart(fig_dist,use_container_width=True)

        if selected_points:
           
            var1.empty()

            df = select_df_points(df_temp,selected_points)
            
            if len(df.index)>=1:
               
                fig4 = make_combined_violin(df_temp,df,point_vis)
                
                with my_expander_dist:
                    st.plotly_chart(fig4,use_container_width=True)
                    
                my_expander_table  = st.beta_expander(label='See Table: ')
            
                with my_expander_table:
                    col_temp1,col_temp2,col_temp3,col_temp4 = st.beta_columns((1,1,1,1))
            
                    vis_button = col_temp1.selectbox('Sort by:',['Cost','Distance'],key='2')
                    if vis_button=='Cost':
                        sort_val = 'Average Charge'
                    if vis_button=='Distance':
                        sort_val = 'Distance'
                    table_md = make_table(df,coordinates,sort_val)
                
                    if len(table_md)<500:
                        col1,col2, col3 = st.beta_columns((1,3,2))
                        col2.markdown(table_md)
                        col_space,col_space2 = st.beta_columns((1,1))
                        col_space.write("")
                    
                    else:
                        st.markdown(table_md)
                  
        col_space,col_space2 = st.beta_columns((1,1))
        col_space.write("")
        col1_a, col3_a = st.beta_columns((2,3))
        if len(cpt_pick)>1:
            cpt_text = [str(int(val)) for val in cpt_pick]
            col1_a.write('CPT code: ' + ", ".join(cpt_text))
        else:
            col1_a.write('CPT code: ' + str(int(cpt_pick)))
        col3_a.write( " Based on 2020 data from: [data.chhs.ca.gov](https://data.chhs.ca.gov/dataset/chargemasters/resource/95e415ee-5c11-40b9-b693-ff9af7985a94)")
st.write("*All prices listed here reflect the average billing rate charged by a provider before any insurance adjustments. To estimate your out-of-pocket expenses, refer to the policy & coverage details of any health insurance plans that you may have.")
