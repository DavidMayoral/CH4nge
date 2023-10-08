import pandas as pd
import numpy as np
import json

import plotly.express as px
import plotly.graph_objects as go

#------------------------------------------------------------
#                          INPUT
#------------------------------------------------------------




#------------------------------------------------------------
#                    READING & FILTERING
#------------------------------------------------------------

df_blank = pd.DataFrame(columns=['Lat', 'Lon', 'Date', 'Emission'])

df_hotspots = pd.read_csv('databases/plumes_2022-01-01_2023-01-01.csv', sep=',')

columns_to_keep = ['plume_latitude', 'plume_longitude', 'datetime', 'emission_auto']
df_hotspots = df_hotspots[columns_to_keep]
df_hotspots = df_hotspots.rename(columns={'datetime':'Date',                      # Renaming columns to more descriptive names
                                            'plume_latitude':'Lat',
                                            'plume_longitude':'Lon',
                                            'emission_auto': 'Emission'})
df_hotspots['Date'] = pd.to_datetime(df_hotspots['Date'])
df_hotspots = df_hotspots[np.isfinite(df_hotspots.Emission)]
# df_hotspots = df_hotspots.set_index(['Date'])

column_names = ['State', 'Value']
df_states = [pd.read_csv('databases/states_2022.csv', sep=',', header=None, names=column_names),
             pd.read_csv('databases/states_2022_cap.csv', sep=',', header=None, names=column_names)]

state_fips_mapping = {
    'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06',
    'CO': '08', 'CT': '09', 'DE': '10', 'DC': '11', 'FL': '12', 
    'HI': '15', 'ID': '16', 'IL': '17', 'IN': '18', 'IA': '19',
    'KS': '20', 'KY': '21', 'LA': '22', 'ME': '23', 'MD': '24',
    'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28', 'MO': '29',
    'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33', 'NJ': '34',
    'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38', 'OH': '39',
    'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44', 'SC': '45',
    'SD': '46', 'TN': '47', 'TX': '48', 'UT': '49', 'VT': '50',
    'VA': '51', 'WA': '53', 'WV': '54', 'WI': '55', 'WY': '56',
    'GA': '13', 'PR': '72', 'VI': '78'
}

def state_to_fips(state):
    return state_fips_mapping.get(state, None)

df_states[0]['State_FIPS'] = df_states[0]['State'].apply(state_to_fips)





#------------------------------------------------------------
#                          PLOTS
#------------------------------------------------------------

# FIGURE 0
fig0 = px.scatter_mapbox(df_blank, lat="Lat", lon="Lon", hover_data=["Date", "Emission"],
                        color_discrete_sequence=["red"], zoom=3, height=700)
fig0.update_layout(mapbox_style="open-street-map")
fig0.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig0.write_html("output/map_blank.html")
fig0.write_image("output/map_blank.png")



# FIGURE 1
fig1 = px.scatter_mapbox(df_hotspots, lat="Lat", lon="Lon", hover_data=["Date", "Emission"],
                        color_discrete_sequence=["red"], zoom=3, height=700)
fig1.update_layout(mapbox_style="open-street-map")
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# fig1.show()
fig1.write_html("output/hotspots1.html")


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
fig2.write_html("output/hotspots2.html")
fig2.write_image("output/hotspots2.png")


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
fig2.write_html("output/hotspots_nomap.html")
fig2.write_image("output/hotspots_nomap.png")


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
        # locationmode = 'USA-states',
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
fig3.write_html("output/bubble.html")


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
fig4.write_html("output/state_map.html")
fig4.write_image("output/state_map.png")


# FIGURE 5

fig5 = go.Figure(data=go.Choropleth(
    locations=df_states[1]['State'], # Spatial coordinates
    z = df_states[1]['Value'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "[MT per person]",
))

fig5.update_layout(
    title_text = '2022 US Methane Emissions',
    geo_scope='usa', # limite map scope to USA
)
fig5.write_html("output/state_map_cap.html")

