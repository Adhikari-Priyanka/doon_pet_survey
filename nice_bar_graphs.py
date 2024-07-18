import pandas as pd
import numpy as np
import os
import plotly.express as px
import kaleido
import plotly.io as pio

## Change file path as needed!!!!
wd = 'F:\\github\\doon_pet_survey_graphs\\'

## Load csv files for cat and dog
cat = pd.read_csv(f'{wd}cat_combine.csv')
dog = pd.read_csv(f'{wd}dog_combine.csv')

col_scale = ['#169999','#555486', '#993989', '#113989']

cat_order_dict = {
    'cat_age':['Kitten (0-6 months)','Junior (7 months - 2 years)', 'Adult (3-6 years)','Mature (>7 years)'],
    'cat_sex' : ['Female', 'Male'] ,
    'cat_neutered' : ['Not neutered', 'Neutered'],
    'cat_describe' : ["Indoor-outdoor cat (the cat wanders outside on its own, but you feed it and look after it when it is sick)",'Completely indoor cat (always stays at home and does not go out on its own'],
    'cat_feed_freq' : ['Once a day', 'Twice a day', 'Thrice a day', 'Continuous supply of food' ],
    'cat_time_out': ['Completely indoors', '1-3 hours', '3-5 hours', '5-7 hours', '>7 hours'],
    'cat_stay' : ['At home', 'Either at home or outside', 'Outside'],
    'cat_hunt_yn': ['Yes', 'No'],
    'cat_hunt_yn_fix': ['Yes', 'No'],
    'cat_hunt_fix' : ['Birds','Rodents','Reptiles','Insects','Squirrels','Amphibians'],
    'cat_hunt_freq': ['Once a week', 'Once in 15 days', 'Once a month','Once every few months'], 
    'cat_time': ['<1 hour','1-2 hours','2-4 hours','>4 hours']
    }
dog_order_dict = {
    'dog_age' : ['0-3 months', '3 months - 1 year','1-3 years','3-5 years','5-8 years','8 - 12 years','12 years and older'],
    'dog_sex' : ['Female', 'Male'],
    'dog_neutered' : ['Neutered', 'Not neutered'],
    'dog_hunt_yn' : ['Yes', 'No', 'Have not observed'],
    'dog_hunt_yn_fix': ['Yes', 'No'],
    'dog_hunt_freq' : ['Few times a month','Once every few months']
}

## Define independent and dependent variables (single option columns ONLY)
cat_dep_var = ['cat_hunt_yn_fix', 'cat_hunt_freq']
cat_indep_var = ['cat_sex','cat_neutered',
             'cat_age','cat_time',
             'cat_time_out','cat_stay',
             'cat_feed_freq']

dog_dep_var = ['dog_hunt_yn_fix','dog_hunt_freq']
dog_indep_var = ['dog_neutered', 'dog_sex', 'dog_age']

## Save contingency tables as text file

filename = f'{wd}contingency tables.txt'
if not os.path.isfile(filename):
    # If the file does not exist, create it
    with open(filename, 'w') as file:
        file.write('')  # Create an empty file
    print(f"'{filename}' has been created.")
else:
    print(f"'{filename}' already exists.")

with open(filename,'w') as f: # Open the file
    for dv in cat_dep_var:
        for iv in cat_indep_var:
            res = pd.crosstab(cat[dv],cat[iv]
                              ).reindex(cat_order_dict[dv], columns=cat_order_dict[iv]) 
            f.write(f'CAT Contingency table for {dv} and {iv}: \n{res}\n\n')
    for dv in dog_dep_var:
        for iv in dog_indep_var:
            res = pd.crosstab(dog[dv],dog[iv]
                              ).reindex(dog_order_dict[dv], columns=dog_order_dict[iv]) 
            f.write(f'DOG Contingency table for {dv} and {iv}: \n{res}\n\n')


## Define function to make a bar graph
def nice_graph(df, x_var, col_var, 
               graph_title, x_tit, legend_tit, 
               h, w, 
               an_x,an_y,
               dof, alpha, chi2, crit, p):
    fig = px.histogram(df, x_var, color= col_var,
                   # Graph title
                   title = graph_title, 
                   # Set color sequence
                   color_discrete_sequence= col_scale,
                   # Define required order of categories
                   category_orders= { x_var : cat_order_dict[x_var],
                                     col_var : cat_order_dict[col_var]}, 
                   # Include labels
                   text_auto=True
                   )
    fig.update_yaxes(title = 'Number of cats', # Y-axis title
                 # Set the grid format
                 showline=True, linewidth=1, linecolor='Black',
                 gridcolor='Grey', gridwidth=0.75)
    
    fig.update_xaxes(title = x_tit, # X-axis title
                 showline=True, linewidth=1, linecolor='Black')

    fig.update_layout(showlegend=True, # Display legend
                  # Legend title
                  legend_title_text= legend_tit, 
                  # Background color
                  plot_bgcolor='White', 
                  # Define range of y axis
                  yaxis_range=[0,max(df[x_var].value_counts()*1.1)],
                  # Change size of graph
                  autosize=False,width=w,height=h
                  )

    fig.add_annotation(text=
                   f'Chi2 value= {chi2} <br> alpha= {alpha}, dof={dof} <br> Critical value = {crit} <br> P value = {p}',
                   align = 'left',
                  xref="paper", yref="paper",
                  x=an_x, y=an_y, 
                  bordercolor='Black',borderwidth=1,
                  showarrow=False)
    
     # Save figure as png
    pio.write_image(fig, f'{wd}stack_{x_var}and{col_var}.png', engine="kaleido")
    
    # Display success message
    print(f'Prepared stacked bar graph for {x_var} and {col_var}')
    # fig.show()

########################################################

# 1. Plot of hunting activity of cats across age groups
## cat_hunt_yn_fix and cat_age
## reject h0, there is a relationship 
## Chi square value = 20.20993784642799
## Critical value = 7.814727903251179
## alpha=0.05
## df=3
## P value = 0.0001535581691545218

nice_graph(df= cat, x_var= 'cat_age',
col_var= 'cat_hunt_yn_fix',
graph_title= 'Plot of hunting activity of cats across age groups',
x_tit= 'Cat age groups',
legend_tit= 'Cats that hunt',
h=800,w=800,
an_x=1,an_y=0.74, 
dof=3, alpha=0.05, chi2=20.20, crit=7.81, p='<0.001')


# 2. Plot hunting activity of cats and time spent outside

## cat_hunt_yn_fix and cat_time_out
## reject h0, there is a relationship 
## Chi square value = 28.223985530040895 
## Critical value = 9.487729036781154 
## alpha=0.05
## df=4 
## P value = 1.1234691477124414e-05

nice_graph(df = cat, x_var= 'cat_time_out',
col_var= 'cat_hunt_yn_fix',
graph_title= 'Plot of cat hunting and time spent outside',
x_tit= 'Time spent outside',
legend_tit= 'Cats that hunt',
h=400,w=900,
an_x=1.2,an_y=0.33, 
dof=4, alpha=0.05, chi2=28.22, crit=9.48, p='<0.001')


# 3. Plot hunting activity of cats hunting and cat stay

## Result for cat_hunt_yn_fix and cat_stay: 
## reject h0, there is a relationship 
## Chi square value = 6.434185477710145
## Critical value = 5.991464547107979
## alpha=0.05
## df=2 
## P value = 0.040071387066250796

nice_graph(df = cat, x_var= 'cat_stay',
col_var= 'cat_hunt_yn_fix',
graph_title= 'Plot of cat hunting and cat stay',
x_tit= 'Cat stay',
legend_tit= 'Cats that hunt',
h=500,w=800,
an_x=1.23,an_y=0.33, 
dof=2, alpha=0.05, chi2=6.43, crit=5.99, p=0.04)
 
 
 # 4. Plot hunting activity of cats and feeding frequency

#Result for cat_hunt_yn_fix and cat_feed_freq
## reject h0, there is a relationship 
## Chi square value = 13.090261742154786
## Critical value = 7.814727903251179
## alpha=0.05
## df=3
## P value = 0.004445420000007694

nice_graph(df = cat, x_var= 'cat_feed_freq',
col_var= 'cat_hunt_yn_fix',
graph_title= 'Plot of cat hunting and feeding frequency',
x_tit= 'Feeding frequency',
legend_tit= 'Cats that hunt',
h=800,w=500,
an_x=1.4,an_y=0.81, 
dof=3, alpha=0.05, chi2=13.09, crit=7.81, p=0.004)


# 5. Plot hunting activity of cats and neutered status

#Result for cat_hunt and cat_neutered
## Chi square value = 16.69097222222222
## Critical value = 15.507313055865453
## alpha=0.05
## df=8 
## P value = 0.03349274096630939

# Select only required columns from the dataframe
df1 = cat[['cat_hunt', 'cat_neutered']]
# Remove multiple entries in one line
df1['cat_hunt_fix'] = df1['cat_hunt'].str.split(';')
df2 = df1.explode('cat_hunt_fix').reset_index(drop=True)
# Remove blank values
df3 = df2[df2['cat_hunt_fix']!='']
# Remove text inside ()
df3['cat_hunt_fix'] = df3['cat_hunt_fix'].str.split('(').str.get(0).str.strip()

nice_graph(df = df3, x_var= 'cat_hunt_fix',
col_var= 'cat_neutered',
graph_title= 'Plot of types of prey by cat neutered status',
x_tit= 'Types of prey',
legend_tit= 'Cats neutered status',
h=400,w=800,
an_x=1.3,an_y=0.50, 
dof=8, alpha=0.05, chi2=16.69, crit=15.5, p=0.03)


# 6. Plot hunting activity of cats and cats across age groups

## Result for cat_hunt and cat_age
## reject h0, there is a relationship 
## Chi square value = 16.69097222222222
## Critical value = 15.507313055865453
## alpha=0.05
## df=8
## P value = 0.03349274096630939

# Select only required columns from the dataframe
df1 = cat[['cat_hunt', 'cat_age']]
# Remove multiple entries in one line
df1['cat_hunt_fix'] = df1['cat_hunt'].str.split(';')
df2 = df1.explode('cat_hunt_fix').reset_index(drop=True)
# Remove blank values
df3 = df2[df2['cat_hunt_fix']!='']
# Remove text inside ()
df3['cat_hunt_fix'] = df3['cat_hunt_fix'].str.split('(').str.get(0).str.strip()

nice_graph(df = df3, x_var= 'cat_hunt_fix',
col_var= 'cat_age',
graph_title= 'Plot hunting activity of cats and cats across age groups',
x_tit= 'Types of prey',
legend_tit= 'Cat age groups',
h=400,w=800,
an_x=1.3,an_y=0.2, 
dof=8, alpha=0.05, chi2=16.69, crit=15.50, p=0.03)


