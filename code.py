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


    coord_group['cluster'] = coord_group.cluster.apply(lambda x: str(x))
    
    
    
    fig = exp.scatter_mapbox(

        coord_group, 

        lat = "y", 

        lon = "x",

        color = "cluster", 

        color_discrete_sequence = exp.colors.qualitative.Vivid,

        size = "incident_id", 

        size_max = 15,

        opacity = 0.7,


        mapbox_style = 'carto-darkmatter',


        zoom = 10.5,


        center = dict(lat = 37.773972, lon =  -122.431297),


        # scope = 'usa',

        # fitbounds = 'locations',  


        labels = {"cluster": 'Clusters\n'},


        custom_data=[

            coord_group['x'], coord_group['y'], coord_group['incident_id'], coord_group['cluster'],

            coord_group['neighborhood'], coord_group['zipcode']


        ]



    )


    hovertemp = '<b>Longitude:  </b>%{customdata[0]}<br><br>'


    hovertemp += '<b>Latitude:  </b>%{customdata[1]}<br><br>'


    hovertemp += '<b>Neighborhood:  </b>%{customdata[4]}<br><br>'


    hovertemp += '<b>Zipcode:  </b>%{customdata[5]}<br><br>'


    hovertemp += '<b>Cluster:  </b>%{customdata[3]}<br><br>'


    hovertemp += '<b>Number of Incidents:  </b>%{customdata[2]}<br>'



    fig.update_traces(hovertemplate = hovertemp)


    # fig.update_layout(



    #     title={



    #         'text': "Title Text",

    #         'y':0.9,

    #         'x':0.5,

    #         'xanchor': 'center',   

    #         'yanchor': 'top',


    #         'font': dict(


    #                 family="Arial",


    #                 size=100, 


    #                 color="red"


    #             )


    #         }, 


    #     )




    fig.update_layout(uniformtext_minsize = 12)


    fig.update_layout(width = 1050, height = 500)


    # fig.update_layout(paper_bgcolor = " #1e1e1e")        # Paper: The screen which is not a part of the plot.


    fig.update_layout(legend=dict(
        # x=0,
        # y=1,

        title_font_family="sans-serif",

        title_font_size = 18,

        # title_font_color = "#E2DFD2",

        font=dict(
            family="sans-serif",
            size=16,
            # color="#E2DFD2"
        ),

        # bgcolor="LightBlue",
        # bordercolor="Black",
        borderwidth = 7
    ))



    fig.update_layout(margin = dict(b = 0, l= 0, t = 0, r = 0))


    st.plotly_chart(fig)




def chart_sidebar():


        lars = ['From Vehicle',
                 'Shoplifting',
                 'Other',
                 'From Building',
                 'Bicycle',
                 'Auto Parts',
                 'Pickpocket',
                 'Purse Snatch']



        lars.sort()



        years = [2021 + i for i in range(2)]



        years.sort()



        st.sidebar.markdown(
            '<b class="header-style">Parameters</b>',
            unsafe_allow_html=True
        )





        st.sidebar.markdown(
            '<br>',
            unsafe_allow_html=True
        )



        # st.sidebar.markdown(
        #     '<p class="font-style" style="font-size:14px;">Parameters</>',
        #     unsafe_allow_html=True
        # )



        coord_group_name = st.sidebar.selectbox(


            label = "Select Theft Type", 


            options = lars



            )



        st.sidebar.markdown(
            '<br>',
            unsafe_allow_html=True
        )




        year = st.sidebar.selectbox(


            label = "Select Year", 


            options = years


            )



        st.sidebar.markdown(
            '<br>',
            unsafe_allow_html=True
        )



        n_clusters = st.sidebar.slider(

            label = "Select Number of Clusters", 

            min_value = 2, 

            max_value = 10,

            value = 3


            )

      
        values = [coord_group_name, year, n_clusters]


        with open(f'./model_files/model_{coord_group_name}_{year}_{n_clusters}.pkl', 'rb') as file:


                coord_group = load(file)



        return coord_group






def chart_header():



    st.set_page_config(


        page_title="Centres of Theft in San Franciso (2021 - 2022)",


        layout="wide"


        )




    hide_default_format = """
                               <style>
                               #MainMenu {visibility: hidden; }
                               footer {visibility: hidden;}
                               </style>

                          """


    st.markdown(hide_default_format, unsafe_allow_html=True)






    st.markdown(


            """
            <style>
            .header-style {
                font-size:25px;
                font-family:'Nunito', sans-serif;

            }
            </style>
            """

            ,


            unsafe_allow_html=True


        )

    st.markdown(


            """
            <style>
            .font-style {
                font-size:20px;
                font-family: 'Nunito', sans-serif;

            }
            </style>
            """,


            unsafe_allow_html=True


        )


    st.markdown(

            '<b class="header-style" style="font-size:30px;text-align:center;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Centers of Theft in San Franciso for the Years 2021 and 2022</b>',


            unsafe_allow_html=True

        )










chart_header()


chart_builder(coord_group = chart_sidebar())

