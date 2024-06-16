import pandas as pd
import numpy as np
import plotly.express as px
import kaleido
import plotly.io as pio

# Load cleaned cat sheet
df = pd.read_csv("F:\\github\\doon_pet_survey\\cat_combine.csv")

#Define color scale
col_scale = ['yellow','orange','red','green','blue', 'purple']

#Histogram of cat_ages

## Remove NA values
df1= df.dropna(subset=['cat_age'])
print('length of cleaned df ',len(df1))

##Plot histogram
fig = px.histogram(df1, x='cat_age',
                title="Distribution of cat ages",
                color= 'cat_age',
                color_discrete_sequence= col_scale,
                category_orders= {'cat_age':['Kitten (0-6 months)','Junior (7 months - 2 years)',
                                   'Adult (3-6 years)','Mature (7-10 years)', 'Senior (11-14 years)']}
                )
fig.update_yaxes(title = 'Count') # Y-axis title
fig.update_xaxes(title = 'Cat age groups') # X-axis title
fig. update_layout(showlegend=False) # Remove legend

## Save as png
pio.write_image(fig, 'hist_cat_age.png', engine="kaleido")
