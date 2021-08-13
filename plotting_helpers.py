import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 
import numpy as np
from helpers import calc_dist
import streamlit as st

@st.cache(allow_output_mutation=True,show_spinner=False)
def create_map(df_temp,coordinates,zoom_val,val_1,val_99,token):
    df_temp['Difference']=df_temp['Average Charge']-df_temp['Average Charge'].mean()
    df_temp['const_size']=df_temp['Average Charge'].mean()
    total_hospitals = df_temp['Hospital Name'].nunique()
    fig = px.scatter_mapbox(df_temp, 
        lat="lat", 
        lon="lon", 
        #color="temp_size",
        color="Average Charge",
        size="const_size",
        #size="temp_size",
        color_continuous_scale='ylorrd',
        #color_continuous_scale='RdYlBu_r',
        #color_continuous_midpoint=df_temp['Average Charge'].mean(),
        hover_data ={'lat':False,'lon':False,'Average Charge': True},
        range_color=[val_1,val_99],
        custom_data=['Hospital Name','Average Charge'],
        size_max = 13
        )
    
    template='<b>%{customdata[0]}</b><br>$%{customdata[1]:,.0f}'
    
    fig.update_traces(hovertemplate=template)
    
    fig.update_layout(mapbox_style="dark", 
        mapbox_accesstoken=token,
        margin=dict(l=0, r=0, t=35, b=10),
        coloraxis_colorbar=dict(
            xpad=3,title='',
            tickprefix='$'
            ),
        hovermode='closest',
        mapbox=dict(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=coordinates[0],
                lon=coordinates[1]
                ),
            pitch=15,
            zoom=zoom_val
            )
        )
    fig.add_trace(go.Scattermapbox(lat=np.array(coordinates[0]), lon=np.array(coordinates[1]),
        hovertext=['Your Location'], 
        hoverinfo='text',
        mode='markers',
        marker=dict(symbol ='marker', size=15, color='blue',opacity=.5))
        )
    fig.add_annotation(xref="paper", yref="paper",
            x=0.84, y=1, 
            text="Try making a selection ☝️",
            showarrow=False,
            arrowhead=1,font=dict(
                color="LightYellow", size=14)
                )  
    # fig.add_annotation(xref="paper", yref="paper",
            # x=0, y=1, 
            # text="Displaying " + str(total_hospitals) + " hospitals",
            # showarrow=False,
            # arrowhead=1,font=dict(
                # color="LightYellow", size=14)
                # )          
    fig.update_traces(showlegend=False)

    return fig
    
@st.cache(allow_output_mutation=True,show_spinner=False)
def create_map_base(df_temp,coordinates,zoom_val,token):
    df_temp['const_size']=df_temp['Average Charge'].mean()
    total_hospitals = df_temp['Hospital Name'].nunique()
    df_temp = df_temp[df_temp['Item Name']=='']
    fig = px.scatter_mapbox(df_temp, 
        lat="lat", 
        lon="lon", 
        size="const_size",
        hover_data ={'lat':False,'lon':False,'Average Charge': False},
        size_max = 0.001
        )
    
    fig.update_layout(mapbox_style="dark", 
        mapbox_accesstoken=token,
        margin=dict(l=0, r=0, t=35, b=10),
        coloraxis_colorbar=dict(
            xpad=3,title='',
            tickprefix='$'
            ),
        hovermode='closest',
        mapbox=dict(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=coordinates[0],
                lon=coordinates[1]
                ),
            pitch=15,
            zoom=zoom_val
            )
        )
            
    fig.update_traces(showlegend=False)

    return fig
    
@st.cache(allow_output_mutation=True,show_spinner=False)
def map_location(fig,coordinates):
    fig.add_trace(go.Scattermapbox(lat=np.array(coordinates[0]), lon=np.array(coordinates[1]),
        hovertext=['Your Location'], 
        hoverinfo='text',
        mode='markers',
        marker=dict(symbol ='marker', size=15, color='blue',opacity=.5))
        )
    fig.update_traces(showlegend=False)

    return fig


@st.cache(allow_output_mutation=True,show_spinner=False)  
def make_state_violin(df_temp,point_vis):

    df_temp['State']='CA'
    fig_dist = go.Figure()
    fig_dist.add_trace(go.Violin(x=df_temp['State'], y=df_temp['Average Charge'], 
        meanline_visible=True, 
        box_visible=True,
        points = point_vis, 
        customdata = df_temp['Hospital Name'],
        hovertemplate='<b>%{customdata}</b><br>$%{y:,.0f}',
        hoveron = "violins+points",name='')
        )
    fig_dist.update_yaxes(title=dict(text=''),tickprefix='$',side='right')
    fig_dist.update_layout(margin=dict(l=10, r=110, t=25, b=10))
    return fig_dist
     
@st.cache(allow_output_mutation=True,show_spinner=False)
def make_combined_violin(df_temp,df,point_vis):
    df['State']='Selection'
    fig2 = go.Figure()
    fig2.add_trace(go.Violin(x=df_temp['State'], y=df_temp['Average Charge'],
        points = point_vis, 
        meanline_visible=True, 
        box_visible=True,
        customdata = df_temp['Hospital Name'],
        hovertemplate='<b>%{customdata}</b><br>$%{y:,.0f}',
        hoveron = "violins+points",name='')
        )
    fig3 = px.strip(df,x=df['State'], y=df['Average Charge'],
        hover_data = {'State': False,'Average Charge': True,'Hospital Name':False},
        custom_data=['Hospital Name']
        )
    template='<b>%{customdata}</b><br>$%{y:,.0f}'
    fig3.update_traces(hovertemplate=template)
    fig4 = go.Figure(data =  fig3.data + fig2.data)
    fig4.update_yaxes(title=dict(text=''),tickprefix='$',side='right')
    fig4.update_layout(margin=dict(l=10, r=110, t=25, b=10),showlegend=False)
    return fig4
    
@st.cache(allow_output_mutation=True,show_spinner=False) 
def make_table(df,coordinates,sort_val):
    
    def f(x):    
        
        return '[{}] (http://maps.google.com/maps?saddr={:f},{:f}&daddr={:f},{:f} "Google Maps Directions")'.format(x['Distance'],x['lat'], x['lon'] ,coordinates[0],coordinates[1])
       
    df_mark = df[['Hospital Name','Average Charge','lat','lon']].sort_values('Average Charge')
    coord_vals=df_mark[['lat','lon']].values
    dist = [calc_dist(x,coordinates) for x in coord_vals]
    df_mark['Distance_val'] = dist
    df_mark['Distance'] = df_mark['Distance_val'].apply(lambda x: f"{x:.1f} mile" if x==1 else f"{x:,.1f} miles")
    df_mark['Cost']=df_mark['Average Charge'].apply(lambda x: f"${x:,.0f}")
    df_mark['Distance'] = df_mark.apply(f, axis=1)
    if sort_val=='Distance':
        temp = df_mark[['Hospital Name','Cost','Distance','Distance_val']].sort_values('Distance_val')
        table_md = temp[['Hospital Name','Cost','Distance']].to_markdown(index=False)
    else:
        table_md = df_mark[['Hospital Name','Cost','Distance']].to_markdown(index=False)
    return table_md
    