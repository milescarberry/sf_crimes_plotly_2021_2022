import numpy as np

import pandas as pd

from plotly import express as exp


from plotly import graph_objects as go


import streamlit as st


import datetime as dt


from joblib import dump, load


from sklearn.cluster import KMeans


from os import listdir




def chart_builder(coord_group):
    
    
    
    # Building the map scatter plot:
    
    
    
    fig = exp.scatter_geo(

        coord_group, 

        lat = "y", 

        lon = "x", 

        color = "cluster", 

        color_discrete_sequence = exp.colors.qualitative.Plotly,

        size = "incident_id", 

        opacity = 0.7,


        scope = 'usa',


        labels = {"cluster": "Clusters"},


        custom_data=[

            coord_group['x'], coord_group['y'], coord_group['incident_id'], coord_group['cluster'],

            coord_group['neighborhood'], coord_group['zipcode']


        ]



    )


    hovertemp = '<b>Longitude:  </b>%{customdata[0]}<br>'


    hovertemp += '<b>Latitude:  </b>%{customdata[1]}<br>'


    hovertemp += '<b>Neighborhood:  </b>%{customdata[4]}<br>'


    hovertemp += '<b>Zipcode:  </b>%{customdata[5]}<br>'


    hovertemp += '<b>Cluster:  </b>%{customdata[3]}<br>'


    hovertemp += '<b>Number of Incidents:  </b>%{customdata[2]}<br>'



    fig.update_traces(hovertemplate = hovertemp)


    fig.update_layout(title = dict(text = "Larceny Hotspots"))


    st.plotly_chart(fig)




with open('./model_files/model_Auto Parts_10.pkl', 'rb') as file:


    coord_group = load(file)





chart_builder(coord_group = coord_group)