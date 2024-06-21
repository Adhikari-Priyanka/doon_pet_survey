import pandas as pd
import numpy as np
import plotly.express as px
import kaleido
import plotly.io as pio

# Load csv files for cat and dog
cat = pd.read_csv("F:\\github\\doon_pet_survey\\cat_combine.csv")
dog = pd.read_csv("F:\\github\\doon_pet_survey\\dog_combine.csv")

cat_hunt= cat['cat_hunt']
cat_feed= cat['cat_feed']
dog_hunt= dog['dog_hunt']


# Function to generate histograms
def histo_multi(df, var):
    # var is the column name to make histogram for
    # order_dict is a dictionary containing correct order for all categorical values
    
    col_scale = ['yellow','orange','red','green','blue']
    
    # Title for graph
    var_tit = var.replace('_',' ')
    
    # Remove multiple entries in one line
    var_fix = df[var].str.split(';').explode().reset_index(drop=True) 
    # Remove NA values
    var_fix1 = var_fix.dropna()
    # Remove blank values
    var_fix2 = var_fix1[var_fix1!='']
    # Remove text inside ()
    var_fix3 = var_fix2.str.split('(').str.get(0).str.strip()
    
    # Make a histogram
    fig = px.histogram(x=var_fix3,
                       title=f"Distribution of {var_tit}", # Graph title
                       color= var_fix3, # Differently colored bars based on column var
                       color_discrete_sequence= col_scale, # Define color for bars
                       text_auto=True
                       )
    fig.update_yaxes(title = 'Count') # Y-axis title
    fig.update_xaxes(title = var_tit) # X-axis title
    fig. update_layout(showlegend=False) # Remove legend
    
    # Save figure as png
    pio.write_image(fig, f'hist_{var}.png', engine="kaleido")
    
    # Display success message
    print('Prepared histogram for ', var)

histo_multi(cat, 'cat_hunt')
histo_multi(cat,'cat_feed')
histo_multi(dog,'dog_hunt')

