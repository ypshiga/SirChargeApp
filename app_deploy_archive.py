import streamlit as st
from streamlit_plotly_events import plotly_events
import streamlit.components.v1 as components
import json
#Import plotly express and plotly graph_objects
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 
import numpy as np
import os

token = os.environ['TOKEN']

@st.cache(allow_output_mutation=True)
def df_map(item):
    df_temp = appended_df[appended_df["Item Name"]==item].copy()
    selected_points=[]
    return df_temp

def df_select(df_temp,selected_points):
    inds = [x["pointNumber"] for x  in selected_points]
    df = pd.DataFrame(df_temp[['Hospital Name','Average Charge']].iloc[inds])
    return df
    

# Load data and do some filtering
appended_df_base = pd.read_csv('Charge_data_2.csv')
appended_df_base.drop("Unnamed: 0", axis=1, inplace=True) # drop index
df_agg = appended_df_base.groupby(['Item Name','2020 CPT Code'], as_index=False)['Average Charge'].agg(['mean',"std", 'count'])
agg_2 = df_agg.nlargest(20,'count')
list_20 = [val[0] for val in agg_2.index.values]
appended_df=appended_df_base[appended_df_base['Item Name'].isin(list_20)] # subset to top 20 most common

# First streamlit command
st.set_page_config(page_title='Hospital Cost Finder', page_icon="img/clinic-16.png")

#st.title('')
st.header('Find and compare hospital costs in California')


# initial selection for inital plots
item_select = st.selectbox('20 most common services:',list(appended_df['Item Name'].unique()),index=0)
   
lat_init = 36.75
lon_init = -120

my_expander = st.beta_expander(label='Select services')
with my_expander:
    common = st.button('20 Most Common')
    if common:
        'See list above ☝️'
    LAB = st.button('Labs')
    if LAB:
        'Working on this...'
    ER = st.button('Emergency')
    if ER:
        'Working on this...'
    RAD = st.button('Radiology')
    if RAD:
        'Working on this...'
    MED = st.button('Medicine')
    if MED:
        'Working on this...'
cpt_pick = appended_df["2020 CPT Code"][appended_df['Item Name']==item_select].unique()
#st.subheader('Displaying costs for: ' + str(item_select) + '.')
#df_temp = appended_df[appended_df["2020 CPT Code"]==cpt_index].copy()


df_temp = df_map(item_select)
val_99 = np.nanpercentile(df_temp["Average Charge"],99)
val_1 = np.nanpercentile(df_temp["Average Charge"],1)
val_mean = int(np.mean(df_temp["Average Charge"]))
val_min = int(np.min(df_temp["Average Charge"]))
val_max = int(np.max(df_temp["Average Charge"]))

st.subheader(item_select)

st.subheader('Average cost = $' + str(val_mean))
#st.subheader('State-wide average = $' + str(val_mean) + '. Min = $' + str(val_min) + '. Max = $' + str(val_max) + '.')

#df_temp.loc[df_temp["Average Charge"]>val_99, "Average Charge"] = val_99
fig = px.scatter_mapbox(df_temp, lat="lat", lon="lon", color="Average Charge",size="Average Charge",
    color_continuous_scale='ylorrd',hover_data ={'lat':False,'lon':False,'Average Charge': True},
    range_color=[val_1,val_99],custom_data=['Hospital Name','Average Charge'],size_max = 30)
template='<b>%{customdata[0]}</b><br>$%{customdata[1]:,.0f}'
fig.update_traces(hovertemplate=template)
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token,
    title_x=0.5,
    margin=dict(l=0, r=0, t=25, b=10),
    coloraxis_colorbar=dict(
    xpad=3,title='',
    tickprefix='$'),
    hovermode='closest',
    mapbox=dict(
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=lat_init,
            lon=lon_init
        ),
        pitch=15,
        zoom=4.6
    ))
i=0
selected_points = plotly_events(fig, click_event=True,select_event=True,override_width='95%')

#st.plotly_chart(fig,use_container_width=True)

var1 = st.empty()
df_temp['State']='CA'
fig = go.Figure()
fig.add_trace(go.Violin(x=df_temp['State'], y=df_temp['Average Charge'], meanline_visible=True, box_visible=True,points ='all', customdata = df_temp['Hospital Name'],
    hovertemplate='<b>%{customdata}</b><br>$%{y:,.0f}',hoveron = "points",name=''))
fig.update_yaxes(title=dict(text=''),tickprefix='$',side='right')
fig.update_layout(margin=dict(l=10, r=110, t=25, b=10))
var1.plotly_chart(fig,use_container_width=True)
#selected_points_chart = plotly_events(hist, click_event=True,select_event=True,override_width='95%')

# def df_update(df_orig,df_temp,selected_points):
    # inds = [x["pointNumber"] for x  in selected_points]
    # df = pd.DataFrame(df_temp[['Hospital Name','Average Charge']].iloc[inds])
    # return pd.concat(df,df_orig)
    
# def merge_two_dicts(x, y):
    # """Given two dictionaries, merge them into a new dict as a shallow copy."""
    # z = x.copy()
    # z.update(y)
    # return z    


if selected_points:
    var1.empty()
    selected=json.loads(selected_points)
    df = df_select(df_temp,selected)
    df['State']='Selection'
    #df['Cost']=df['Average Charge'].apply(lambda x: f"${x:,.0f}")
   
    if len(df.index)>=1:
        #hist2 = go.Violin(x=df['State'], y=df['Average Charge'],points ='all',width = .1)
        fig2 = go.Figure()
        fig2.add_trace(go.Violin(x=df_temp['State'], y=df_temp['Average Charge'],points ='all', meanline_visible=True, box_visible=True,customdata = df_temp['Hospital Name'],hovertemplate='<b>%{customdata}</b><br>$%{y:,.0f}',hoveron = "points"))
        
        fig3 = px.strip(df,x=df['State'], y=df['Average Charge'],hover_data = {'State': False,'Average Charge': True,'Hospital Name':False},custom_data=['Hospital Name'])
        template='<b>%{customdata}</b><br>$%{y:,.0f}'
        fig3.update_traces(hovertemplate=template)
        fig4 = go.Figure(data=  fig3.data+fig2.data)

        fig4.update_yaxes(title=dict(text=''),tickprefix='$',side='right')
        fig4.update_layout(margin=dict(l=10, r=110, t=25, b=10),showlegend=False)
        st.plotly_chart(fig4,use_container_width=True)

    my_expander_table  = st.beta_expander(label='See Table: ')
    with my_expander_table:
        if len(df.index)>25:
            pass
        else:
            #st.markdown(df[['Hospital Name','Average Charge']].sort_values('Average Charge').rename(columns={'Average Charge':'Cost'}).to_markdown(index=False))
            df_mark = df[['Hospital Name','Average Charge']].sort_values('Average Charge')
            df_mark['Cost']=df_mark['Average Charge'].apply(lambda x: f"${x:,.0f}")
            #
            table_md = df_mark[['Hospital Name','Cost']].to_markdown(index=False)
            if len(table_md)<500:
                col1,col2, col3 = st.beta_columns((1,3,2))
                col2.markdown(table_md)
                col_space,col_space2 = st.beta_columns((1,1))
                col_space.write("")
            else:
                st.markdown(table_md)
                col_space,col_space2 = st.beta_columns((1,1))
                col_space.write("")

    
col_space,col_space2 = st.beta_columns((1,1))
col_space.write("")
col1_a,col2_a, col3_a = st.beta_columns((1,1,3))
col1_a.write('CPT code: ' + str(int(cpt_pick)))
col3_a.write( " Based on 2020 data from: [data.chhs.ca.gov](https://data.chhs.ca.gov/dataset/chargemasters/resource/95e415ee-5c11-40b9-b693-ff9af7985a94)")
