import numpy as np

import pandas as pd

from plotly import express as exp


from plotly import graph_objects as go


import streamlit as st


import datetime as dt


from joblib import dump, load


from sklearn.cluster import KMeans


from os import listdir




def get_neigh_df():
    
    
    neigh_df = pd.read_csv("./san_francisco_crimes_data_from_2018/address_list_neigh.csv")


    lats = neigh_df.latitude_.values.tolist()


    longs= neigh_df.longitude_.values.tolist()


    coords = [(longs[i], lats[i]) for i in range(len(longs))]


    neigh_df['coordinates_'] = coords
    
    
    return neigh_df
    




def model_builder(lar, clusters):
    
    
    with open("./model_files/"+listdir('./model_files')[1], 'rb') as file:
    

        lar_df = load(file)
    
    
    lar_df = lar_df.drop(columns = ['coordinates_'])
    
    
    coord_group = lar_df[lar_df.incident_subcategory == lar].groupby('coordinates').agg({"incident_id": pd.Series.nunique}).reset_index().sort_values(by = "incident_id", ascending = False).reset_index(drop = True)
    
    
    coord_group['x'] = coord_group.coordinates.apply(lambda x: x[0])

    
    coord_group['y'] = coord_group.coordinates.apply(lambda x: x[1])
    
    
    coord_group = pd.merge(coord_group, get_neigh_df(), how = 'left', left_on = "coordinates", right_on = "coordinates_").drop(columns = ["latitude_", "longitude_", "incident_id_", "coordinates_"])

    
    coord_group['zipcode'] = coord_group.zipcode.apply(lambda x: int(x))
    
    
    
    # Building the model:
    
    
    kmeans = KMeans(n_clusters = clusters)
    
    
    kmeans.fit(coord_group[['x', 'y']].to_numpy(), sample_weight = coord_group.incident_id)
    
    
    coord_group['cluster'] = kmeans.labels_
    
    
    return chart_builder(coord_group = coord_group)






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


    hovertemp = '<b>Longitude: </b>%{customdata[0]}<br>'


    hovertemp += '<b>Latitude: </b>%{customdata[1]}<br>'


    hovertemp += '<b>Neighborhood: </b>%{customdata[4]}<br>'


    hovertemp += '<b>Zipcode: </b>%{customdata[5]}<br>'


    hovertemp += '<b>Cluster: </b>%{customdata[3]}<br>'


    hovertemp += '<b>Number of Incidents: </b>%{customdata[2]}<br>'



    fig.update_traces(hovertemplate = hovertemp)


    fig.update_layout(title = dict(text = "Larceny Hotspots"))


    fig.update_layout(margin = dict(b = 0, l = 0, t = 0, r = 0))


    st.plotly_chart(fig)










model_builder("From Vehicle", clusters = 10)

    


