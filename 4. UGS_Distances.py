import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import statistics as st
import plotly.express as px
import kaleido
import plotly.io as pio
import os

## Change file path as needed!!!!
wd = 'F:\\github\\doon_pet_survey_graphs\\'
## Change col_scale 
col_scale = ['#b57edc', '#b6d7a8', '#f1c232']

# Load pet survey data
hunt_freq = gpd.read_file(f'{wd}add_cat_hunt_freq.gpkg')
hunt = gpd.read_file(f'{wd}add_cat_hunt.gpkg')

# Load UGS
ugs = gpd.read_file(f'{wd}ugs_polygon.gpkg')

# Create empty dataframe to store results
result = pd.DataFrame(columns= ['distance', 'site']) 

# Create folder to store boxplots
filepath = f'{wd}\\distance_boxplots\\'
if not os.path.exists(filepath):
    os.makedirs(filepath)

##############################################################

# 1. Calculate the distance to the closest UGC for each point
for i in range(0, len(hunt)):
    # Extract every row as a point
    a = Point(hunt['geometry'].iloc[i])
    # Calculate distances to all UGS points
    b= ugs.distance(a)
    # Create a dataframe of the distance, site and point name
    c = pd.DataFrame({'distance' : b/10**3, 'site':ugs['site']})
    # Find the shortest distance
    d = c.iloc[c['distance'].idxmin()]
    # Extract information about the row i   
    e = pd.Series([hunt['row_ids'].iloc[i], hunt['cat_hunt'].iloc[i]])
    # Concat distance and row information
    f = pd.concat([d,e])
    # Transpose to append to result dataframe
    g = pd.DataFrame(f).transpose()
    result= pd.concat([result,g], axis=0)

## Rename columns appropraitely
result = result.rename(columns={0 : 'row_ids', 1: 'cat_hunt'})
## Write the dataframe to csv
result.to_csv(f'{filepath}cat_hunt_add_dist.csv')

############################################################

# 2. Make a boxplot

## Extract datframe of only hunted birds
res_birds = result[result['cat_hunt'] == 'Birds']

fig = px.box(res_birds, y='distance',
             # Graph title
             title='Plot of distance from urban greenspaces <br>and hunting of birds by cats', 
             # Define color for bars
             color_discrete_sequence= col_scale 
             )
fig.update_yaxes(title = 'Distance (km)', # Y-axis title
                showline=True, linewidth=1, linecolor='Black', 
                gridcolor='Grey', gridwidth=0.75,
                zeroline=True, zerolinewidth=1, zerolinecolor='Black',
                range=[0,5], autorange=False,
                tick0=1, dtick=1)
fig.update_xaxes(title = 'Hunting of birds by cats') # X-axis title
fig.update_layout(plot_bgcolor='White',
                  # Change size of graph
                  autosize=False,width=400,height=500)

# Add means and anova results on box plot
m1 = round(st.mean(res_birds['distance']),2)
m2 = round(st.median(res_birds['distance']),2)
m3 = round(max(res_birds['distance']),2)
m4 = round(min(res_birds['distance']),2)

fig.add_annotation(text = f'Mean={m1}km<br>Median={m2}km<br>Max={m3}km<br>Min={m4}km<br>',
                   align = 'left',
                   xref="paper", yref="paper",
                   x=1.3, y=1.05,
                   bordercolor='Black',borderwidth=1,
                   showarrow=False)

# Save figure as png
pio.write_image(fig, f'{filepath}bird_dist_boxplot.png', engine="kaleido")

############################################################

# 3. Quick graphs

## Cat hunt
fig = px.box(result, x=result['cat_hunt'],y='distance')

# Save figure as png
pio.write_image(fig, f'{wd}hunt_dist_boxplot.png', engine="kaleido")

## Cat hunt freq

res2 = pd.DataFrame(columns= ['distance', 'site']) 

for i in range(0, len(hunt_freq)):
    a = Point(hunt_freq['geometry'].iloc[i])
    b= ugs.distance(a)
    c = pd.DataFrame({'distance' : b/10**3, 'site':ugs['site']})
    d = c.iloc[c['distance'].idxmin()]
    e = pd.Series([hunt_freq['row_ids'].iloc[i], hunt_freq['cat_hunt_freq'].iloc[i]])
    f = pd.concat([d,e])
    g = pd.DataFrame(f).transpose()
    res2= pd.concat([res2,g], axis=0)

res2 = res2.rename(columns={0 : 'row_ids', 1: 'cat_hunt_freq'})
print(len(res2))

res2.to_csv(f'{wd}cat_hunt_freq_add_dist.csv')

fig = px.box(res2, x='cat_hunt_freq', y='distance')

# Save figure as png
pio.write_image(fig, f'{filepath}hunt_freq_dist_boxplot.png', engine="kaleido")
