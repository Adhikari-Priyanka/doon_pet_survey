import pandas as pd
import numpy as np
import plotly.express as px
import kaleido
import plotly.io as pio

## Change file path as needed!!!!
wd = 'F:\\github\\doon_pet_survey_graphs\\histograms\\'

# Load csv files for cat and dog
cat = pd.read_csv("F:\\github\\doon_pet_survey\\cat_combine.csv")
dog = pd.read_csv("F:\\github\\doon_pet_survey\\dog_combine.csv")


# Function to generate histograms

def histo(df, var, order_dict):
    # df is the dataframe to use - cat or dog
    # var is the column name to make histogram for
    # order_dict is a dictionary containing correct order for all categorical values
    
    col_scale = ['yellow','orange','red','green','blue']
    
    # Title for graph
    var_tit = var.replace('_',' ')
    
    # Remove NA values from dataframe as per selected column 'var'
    df = df.replace('', np.nan)
    df1 = df.dropna(subset=[var])
    
    # Make a histogram
    fig = px.histogram(df1, x=var,
                       title=f"Distribution of {var_tit}", # Graph title
                       color= var, # Differently colored bars based on column var
                       color_discrete_sequence= col_scale, # Define color for bars
                       category_orders= { var : order_dict[var]}, # Define required order of categories
                       text_auto=True ## dimension
                       )
    fig.update_yaxes(title = 'Count') # Y-axis title
    fig.update_xaxes(title = var_tit) # X-axis title
    fig. update_layout(showlegend=False) # Remove legend
    
    # Save figure as png
    pio.write_image(fig, f'{wd}hist_{var}.png', engine="kaleido")
    
    # Display success message
    print('Prepared histogram for ', var)



# write a dictionary of column names and specific order for cat.csv
cat_order_dict = {
    'cat_age':['Kitten (0-6 months)','Junior (7 months - 2 years)', 'Adult (3-6 years)','Mature (7-10 years)', 'Senior (11-14 years)'],
    'cat_sex' : ['Female', 'Male'] ,
    'cat_neutered' : ['Neutered', 'Not neutered'],
    'cat_describe' : ["Indoor-outdoor cat (the cat wanders outside on its own, but you feed it and look after it when it is sick)",'Completely indoor cat (always stays at home and does not go out on its own'],
    'cat_feed_freq' : ['Continuous supply of food is available', 'Thrice a day', 'Twice a day', 'Once a day'],
    'cat_time_out': ['1-3 hours', '3-5 hours', '5-7 hours', '7- 10 hours', '>10 hours', 'Completely indoors',"I don't know"],
    'cat_stay' : ['At home', 'Outside', 'Either at home or outside'],
    'cat_hunt_yn': ['Yes', 'No', 'Have not observed'],
    'cat_hunt_freq': ['Once every few months', 'Once a month', 'Once in 15 days', 'Once a week', 'Every day'], ## opposite
    'cat_time': ['None at all', '10-20 minutes', '20-40 minutes','40 minutes-1 hour','1-2 hours','2-4 hours','>4 hours']
    }

# Make histograms for each column in cat.csv
for col_name in cat.columns[2:]:
    try:
        print('graph for ', col_name)
        histo(df=cat, var=col_name, order_dict=cat_order_dict)
    except:
        print('could not make graph for ', col_name)
        pass


# write a dictionary of column names and specific order for dog.csv
dog_order_dict = {
    'dog_age' : ['0-3 months', '3 months - 1 year','1-3 years','3-5 years','5-8 years','8 - 12 years','12 years and older'],
    'dog_sex' : ['Female', 'Male'],
    'dog_neutered' : ['Neutered', 'Not neutered'],
    'dog_hunt_yn' : ['Yes', 'No', 'Have not observed'],
    'dog_hunt_freq' : ['Once every few months','Once a month','Once in 15 days','Once a week','Everyday']
}


# Make histograms for each column in dog.csv
for col_name in dog.columns[2:]:
    try:
        print('graph for ', col_name)
        histo(df=dog, var=col_name, order_dict=dog_order_dict)
    except:
        print('could not make graph for ', col_name)
        pass