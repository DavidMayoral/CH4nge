import pandas as pd
import numpy as np
import os

import plotly.express as px
import plotly.graph_objects as go

#------------------------------------------------------------
#                          INPUT
#------------------------------------------------------------

input_folder = 'dataframes'
input_ext = '.csv'

files = ['df_blank',
         'df_hotspots',
         'df_states1',
         'df_states2']

output_folder = 'output'

#------------------------------------------------------------
#                    DATA IMPORTING
#------------------------------------------------------------
print("\nStarting importing data")

df_blank = pd.read_csv(os.path.join(input_folder, files[0] + input_ext))
df_hotspots = pd.read_csv(os.path.join(input_folder, files[1] + input_ext))
df_states = [pd.read_csv(os.path.join(input_folder, files[2] + input_ext)),
             pd.read_csv(os.path.join(input_folder, files[3] + input_ext))]

print("Importing data terminated")

#------------------------------------------------------------
#                       PLOTTING
#------------------------------------------------------------
print("\nStarting generating plots")

# FIGURE 0
fig0 = px.scatter_mapbox(df_blank, lat="Lat", lon="Lon", hover_data=["Date", "Emission"],
                        color_discrete_sequence=["red"], zoom=3, height=700)
fig0.update_layout(mapbox_style="open-street-map")
fig0.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# FIGURE 1
fig1 = px.scatter_mapbox(df_hotspots, lat="Lat", lon="Lon", hover_data=["Date", "Emission"],
                        color_discrete_sequence=["red"], zoom=3, height=700)
fig1.update_layout(mapbox_style="open-street-map")
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# FIGURE 2
fig2 = px.scatter_mapbox(df_hotspots, lat="Lat", lon="Lon", hover_name="Date", hover_data=["Date", "Emission"],
                        color_discrete_sequence=["red"], zoom=3, height=700)
fig2.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# FIGURE 2b
fig2 = px.scatter_mapbox(df_hotspots, lat="Lat", lon="Lon", hover_name="Date", hover_data=["Date", "Emission"],
                        color_discrete_sequence=["red"], zoom=3, height=700)
fig2.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            # "sourcetype": "raster",
            # "sourceattribution": "United States Geological Survey",
            # "source": [
            #     "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            # ]
        }
      ])
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# FIGURE 3
df_hotspots['text'] = 'Emissions ' + (df_hotspots['Emission']).astype(str)+' [units]'
limits = [(0,50),(51,100),(101,200),(201,500),(501,100000)]
colors = px.colors.sequential.Plasma_r
cities = []
scale = 50

fig3 = go.Figure()

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df_hotspots[lim[0]:lim[1]]
    fig3.add_trace(go.Scattergeo(
        # loc
        # ationmode = 'USA-states',
        lon = df_sub['Lon'],
        lat = df_sub['Lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['Emission']/scale,
            color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1])))

fig3.update_layout(
        title_text = '2022 Methane Emissions<br>(Click legend to toggle traces)',
        showlegend = True
        # geo = dict(
        #     scope = 'usa',
        #     landcolor = 'rgb(217, 217, 217)',
        # )
    )


# FIGURE 4
fig4 = go.Figure(data=go.Choropleth(
    locations=df_states[0]['State'], # Spatial coordinates
    z = df_states[0]['Value'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "[MT CO2-eq]",
))

fig4.update_layout(
    title_text = '2022 US Methane Emissions',
    geo_scope='usa', # limite map scope to USA
)


# FIGURE 5
fig5 = go.Figure(data=go.Choropleth(
    locations=df_states[1]['State'], # Spatial coordinates
    z = df_states[1]['Value'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "[MT per person]"
))

fig5.update_layout(
    title_text = '2022 US Methane Emissions',
    geo_scope='usa', # limite map scope to USA
)

print("Plot generation terminated")

#------------------------------------------------------------
#                       EXPORTING
#------------------------------------------------------------
print("\nStarting exporting plots")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

fig0.write_html(os.path.join(output_folder, "map_blank.html"))
fig0.write_image(os.path.join(output_folder, "map_blank.png"))

fig1.write_html(os.path.join(output_folder, "hotspots1.html"))
fig1.write_image(os.path.join(output_folder, "hotspots1.html"))

fig2.write_html(os.path.join(output_folder, "hotspots2.html"))
fig2.write_image(os.path.join(output_folder, "hotspots2.png"))

fig3.write_html(os.path.join(output_folder, "bubble.html"))
fig3.write_image(os.path.join(output_folder, "bubble.png"))

fig4.write_html(os.path.join(output_folder, "state_map.html"))
fig4.write_image(os.path.join(output_folder, "state_map.png"))

fig5.write_html(os.path.join(output_folder, "state_map_cap.html"))
fig5.write_image(os.path.join(output_folder, "state_map_cap.png"))

print("Plot exporting terminated")