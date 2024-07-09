import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import chi2
import os
import plotly.express as px
import kaleido
import plotly.io as pio

## Change file path as needed!!!!
wd = 'F:\\github\\doon_pet_survey_graphs\\'

## Load csv files for cat and dog
cat = pd.read_csv(f'{wd}cat_combine.csv')
dog = pd.read_csv(f'{wd}dog_combine.csv')

col_scale = ['#999999','#566455']

#########################################################################

# 1. Initialize

## Define independent and dependent variables (single option columns ONLY)
cat_dep_var = ['cat_hunt_yn_fix', 'cat_hunt_freq']
cat_indep_var = ['cat_sex','cat_neutered',
             'cat_age','cat_time',
             'cat_time_out','cat_stay',
             'cat_feed_freq']

dog_dep_var = ['dog_hunt_yn_fix','dog_hunt_freq']
dog_indep_var = ['dog_neutered', 'dog_sex', 'dog_age']

cat_order_dict = {
    'cat_age':['Kitten (0-6 months)','Junior (7 months - 2 years)', 'Adult (3-6 years)','Mature (>7 years)'],
    'cat_sex' : ['Female', 'Male'] ,
    'cat_neutered' : ['Neutered', 'Not neutered'],
    'cat_describe' : ["Indoor-outdoor cat (the cat wanders outside on its own, but you feed it and look after it when it is sick)",'Completely indoor cat (always stays at home and does not go out on its own'],
    'cat_feed_freq' : ['Once a day', 'Twice a day', 'Thrice a day', 'Continuous supply of food is available' ],
    'cat_time_out': ['Completely indoors', '1-3 hours', '3-5 hours', '5-7 hours', '>7 hours'],
    'cat_stay' : ['At home', 'Outside', 'Either at home or outside'],
    'cat_hunt_yn': ['Yes', 'No'],
    'cat_hunt_yn_fix': ['Yes', 'No'],
    'cat_hunt_freq': ['Once a week', 'Once in 15 days', 'Once a month','Once every few months'], 
    'cat_time': ['<20 minutes', '20 minutes-1hour','1-2 hours','2-4 hours','>4 hours']
    }
dog_order_dict = {
    'dog_age' : ['0-3 months', '3 months - 1 year','1-3 years','3-5 years','5-8 years','8 - 12 years','12 years and older'],
    'dog_sex' : ['Female', 'Male'],
    'dog_neutered' : ['Neutered', 'Not neutered'],
    'dog_hunt_yn' : ['Yes', 'No', 'Have not observed'],
    'dog_hunt_yn_fix': ['Yes', 'No'],
    'dog_hunt_freq' : ['Few times a month','Once every few months']
}

#########################################################################

# 2.1 Chi-square test for single option variables

## Define a function that runs chisq for two pandas series

def run_chi2(df, s1, s2, alpha=0.05):
    # df is the dataframe to use
    # s1 and s2 are the column names to use
    # alpha is required value either 0.05 or 0.01, default 0.05
    
    c_tab = pd.crosstab(df[s1], df[s2]) # Create contingency table
    obs = c_tab.values # Observed values
    vals = stats.chi2_contingency(c_tab) # Run Chi2 test of independence of variables
    exp = vals[3] # Expected values
    
    norow = len(c_tab) # No of rows in c_tab
    nocol = len(c_tab.columns) # No of cols in c_tab
    dof = (norow-1) * (nocol-1) # Degree of freedom
    
    chi_sq = sum([(o-e)**2/e for o,e in zip(obs,exp)]).sum() # Find chi2 value
    crit = chi2.ppf(q = 1-alpha, df=dof) # Find critical value using alpha and degree of freedom
    
    pval = 1-chi2.cdf(x=chi_sq, df =dof) # Find P value
    
    if chi_sq >= crit:
          chi_sq_result = 'reject h0, there is a relationship'
    else:
        chi_sq_result = 'accept h0, there is no  relationship'
    if pval <= alpha:
        pval_result = 'reject h0, there is a relationship'
    else:
        pval_result = 'accept h0, there is no relationship'
    
    # Return results and variables as string 
    return f'{chi_sq_result} Chi square value = {chi_sq} and Critical value = {crit} {pval_result} as P value = {pval}\n'


## Run the chi square test for all combinations of dependent and independent variables
## And save as a text file

## For cats
filename_cat = f'{wd}chisq_test_cat.txt' # Name of txt file to store results
if not os.path.isfile(filename_cat):
    # If the file does not exist, create it
    with open(filename_cat, 'w') as file:
        file.write('')  # Create an empty file
    print(f"'{filename_cat}' has been created.")
else:
    print(f"'{filename_cat}' already exists.")

with open(filename_cat,'w') as f: # Open the file
    # Run chi2 test for each combination of dependent and independent variables as defined
    for dv in cat_dep_var:
        for iv in cat_indep_var:
            res = run_chi2(df= cat, s1=dv, s2=iv, alpha = 0.05) # Define alpha
            f.write(f'Result for {dv} and {iv}: \n{res}\n\n')

## For dogs
filename_dog = f'{wd}chisq_test_dog.txt' # Name of txt file to store results
if not os.path.isfile(filename_dog):
    # If the file does not exist, create it
    with open(filename_dog, 'w') as file:
        file.write('')  # Create an empty file
    print(f"'{filename_dog}' has been created.")
else:
    print(f"'{filename_dog}' already exists.")

with open(filename_dog,'w') as f:# Open the file
    # Run chi2 test for each combination of dependent and independent variables as defined
    for dv in dog_dep_var:
        for iv in dog_indep_var:
            res = run_chi2(df= dog, s1=dv, s2=iv, alpha = 0.05) # Define alpha
            f.write(f'Result for {dv} and {iv}: \n{res}\n\n')

# 2.2 Save contingency tables as text file

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


#########################################################################

# 3. Chi-square test for multiple option variables

## Define a function that runs chisq for two pandas series: single option column and one multi option column

def run_chi2_multi(df, s1, multi, alpha=0.05):
    # df is the dataframe to use
    # s1 is the independent variable column names to use
    # multi is the dependent variable column with multiple options
    # alpha is required value either 0.05 or 0.01, default value =0.05
        
    # Select only required columns from the dataframe
    df1 = df[[s1,multi]]
    # Remove multiple entries in one line
    df1['fix'] = df1[multi].str.split(';')
    df2 = df1.explode('fix').reset_index(drop=True)
    # Remove blank values
    df3 = df2[df2['fix']!='']
    # Remove text inside ()
    df3['fix'] = df3['fix'].str.split('(').str.get(0).str.strip()
    
    c_tab = pd.crosstab(df2[s1],df2['fix']) # Create contingency table
    obs = c_tab.values # Observed values
    vals = stats.chi2_contingency(c_tab) # Run Chi2 test of independence of variables
    exp = vals[3] # Expected values
    
    norow = len(c_tab) # No of rows in c_tab
    nocol = len(c_tab.columns) # No of cols in c_tab
    dof = (norow-1) * (nocol-1) # Degree of freedom
    
    chi_sq = sum([(o-e)**2/e for o,e in zip(obs,exp)]).sum() # Find chi2 value
    crit = chi2.ppf(q = 1-alpha, df=dof) # Find critical value using alpha and degree of freedom
    
    pval = 1-chi2.cdf(x=chi_sq, df =dof) # Find P value
    
    if chi_sq >= crit:
          chi_sq_result = 'reject h0, there is a relationship'
    else:
        chi_sq_result = 'accept h0, there is no  relationship'
    if pval <= alpha:
        pval_result = 'reject h0, there is a relationship'
    else:
        pval_result = 'accept h0, there is no relationship'
    
    # Return results and variables as string 
    return f'{chi_sq_result} Chi square value = {chi_sq} and Critical value = {crit} {pval_result} as P value = {pval}\n'


## Chi2 test of cat_hunt (multiple option dependent variable) vs all cat independent variables

filename_cat = f'{wd}chisq_test_cat_hunt.txt' # Name of txt file to store results
if not os.path.isfile(filename_cat):
    # If the file does not exist, create it
    with open(filename_cat, 'w') as file:
        file.write('')  # Create an empty file
    print(f"'{filename_cat}' has been created.")
else:
    print(f"'{filename_cat}' already exists.")

with open(filename_cat,'w') as f: # Open file
    # Run chi2 test for each combination of cat_hunt and independent variables as defined
    for iv in cat_indep_var:
        res = run_chi2_multi(df= cat, s1=iv, multi='cat_hunt', alpha = 0.05) # Define alpha
        f.write(f'Result for cat_hunt and {iv}: \n{res}\n\n')


## Chi2 test of cat_hunt (multiple option dependent variable) vs all cat independent variables

filename_dog = f'{wd}chisq_test_dog_hunt.txt' # Name of txt file to store results
if not os.path.isfile(filename_dog):
    # If the file does not exist, create it
    with open(filename_dog, 'w') as file:
        file.write('')  # Create an empty file
    print(f"'{filename_dog}' has been created.")
else:
    print(f"'{filename_dog}' already exists.")

with open(filename_dog,'w') as f:# Open file
    # Run chi2 test for each combination of dog_hunt and independent variables as defined
    for iv in dog_indep_var:
        res = run_chi2_multi(df= dog, s1=iv, multi='dog_hunt', alpha = 0.05) # Define alpha
        f.write(f'Result for dog_hunt and {iv}: \n{res}\n\n')


## Chi2 test of cat_hunt (multiple option dependent variable) vs cat_feed (multiple option independent variable)

### Create new dataframe with only 'cat_hunt' and 'cat_feed'
df = cat[['cat_hunt','cat_feed']]
## 'cat_hunt'
### Remove multiple entries in one line
df['cat_hunt_fix'] = df['cat_hunt'].str.split(';')
df2 = df.explode('cat_hunt_fix').reset_index(drop=True)
### Remove blank values
df3 = df2[df2['cat_hunt_fix']!='']

## 'cat_feed'
### Remove multiple entries in one line
df3['cat_feed_fix'] = df3['cat_feed'].str.split(';')
df4 = df3.explode('cat_feed_fix').reset_index(drop=True)
### Remove blank values
df5 = df4[df4['cat_feed_fix']!='']

### Remove NA values
df5 = df5.dropna()
### Remove string inside brackets '(.......)'
df5['cat_feed_fix'] = df5['cat_feed_fix'].str.split('(').str.get(0).str.strip()
df5['cat_hunt_fix'] = df5['cat_hunt_fix'].str.split('(').str.get(0).str.strip()

alpha = 0.05 # Define alpha
c_tab = pd.crosstab(df5['cat_feed_fix'],df5['cat_hunt_fix']) # Create contingency table
obs = c_tab.values # Observed values
vals = stats.chi2_contingency(c_tab) # Run Chi2 test of independence of variables
exp = vals[3] # Expected values

norow = len(c_tab) # No of rows in c_tab
nocol = len(c_tab.columns) # No of cols in c_tab
dof = (norow-1) * (nocol-1) # Degree of freedom

chi_sq = sum([(o-e)**2/e for o,e in zip(obs,exp)]).sum() # Find chi2 value
crit = chi2.ppf(q = 1-alpha, df=dof) # Find critical value using alpha and degree of freedom
    
pval = 1-chi2.cdf(x=chi_sq, df =dof) # Find P value

if chi_sq >= crit:
    chi_sq_result = 'reject h0, there is a relationship'
else:
    chi_sq_result = 'accept h0, there is no  relationship'
if pval <= alpha:
    pval_result = 'reject h0, there is a relationship'
else:
    pval_result = 'accept h0, there is no relationship'

with open(filename_cat, 'a') as f: # Open previous file and append
    # Return results and variables as string 
    f.write('Result for cat_hunt and cat_feed: \n')
    f.write(f'{chi_sq_result} Chi square value = {chi_sq} and Critical value = {crit} {pval_result} as P value = {pval}\n')

#########################################################################

# 4. Stacked bar graphs

## Define tuples of variable combinations
graph_vars = [('cat_hunt_yn_fix', 'cat_age'),
('cat_hunt_yn_fix', 'cat_time_out'),
('cat_hunt_yn_fix', 'cat_feed_freq'),
('cat_neutered','cat_hunt_freq')]

graph_multi = [('cat_neutered', 'cat_hunt'), ('cat_stay', 'cat_hunt')]  

## Define function to make a stacked bar graph 
def histo_stack(df, x_var, col_var):
    fig = px.histogram(df, x_var, color= col_var,
                   title = f'Plot {x_var} and {col_var}', # Graph title
                   color_discrete_sequence= col_scale,
                   pattern_shape=col_var,
                   category_orders= { x_var : cat_order_dict[x_var]}, # Define required order of categories
                    text_auto=True ## dimension                   
                   )
    
    fig.update_yaxes(title = 'Count', # Y-axis title
                    showline=True, linewidth=1, linecolor='Black', 
                    gridcolor='Grey', gridwidth=0.75,
                    zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    
    fig.update_xaxes(title = x_var) # X-axis title
    
    fig.update_layout(showlegend=True, # legend
                      plot_bgcolor='White',
                      yaxis_range=[0,
                                   max(df[x_var].value_counts()*1.1)])
    
    # Save figure as png
    pio.write_image(fig, f'{wd}hist_{x_var}and{col_var}.png', engine="kaleido")
    
    # Display success message
    print(f'Prepared histogram for {x_var} and {col_var}')

## Make bar graphs for single option variables
for n in range(len(graph_vars)):
    histo_stack(df=cat, x_var=graph_vars[n][1], col_var=graph_vars[n][0])

## Define function to make a stacked bar graph for multiple option columns
def histo_stack(df, x_var, col_var):
    # Select only required columns from the dataframe
    df1 = df[[x_var, col_var]]
    # Remove multiple entries in one line
    df1['fix'] = df1[x_var].str.split(';')
    df2 = df1.explode('fix').reset_index(drop=True)
    # Remove blank values
    df3 = df2[df2['fix']!='']
    # Remove text inside ()
    df3['fix'] = df3['fix'].str.split('(').str.get(0).str.strip()
    
    fig = px.histogram(df3, 'fix', color= col_var,
                   title = f'Plot {x_var} and {col_var}', # Graph title
                   #color_discrete_sequence= col_scale,
                   #pattern_shape=col_var,
                   category_orders= { x_var : cat_order_dict[x_var]}, # Define required order of categories
                    text_auto=True ## dimension                   
                   )
    fig.update_yaxes(title = 'Count', # Y-axis title
                    showline=True, linewidth=1, linecolor='Black', 
                    gridcolor='Grey', gridwidth=0.75,
                    zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig.update_xaxes(title = x_var) # X-axis title
    fig.update_layout(showlegend=True, # legend
                      plot_bgcolor='White',
                      yaxis_range=[0,
                                   max(df3['fix'].value_counts()*1.1)])
    

    # Save figure as png
    pio.write_image(fig, f'{wd}hist_{x_var}and{col_var}.png', engine="kaleido")
    
    # Display success message
    print(f'Prepared histogram for {x_var} and {col_var}')

## Bar graphs for multiple option columns
histo_stack(cat, x_var = graph_multi[0][1], col_var = graph_multi[0][0])
histo_stack(cat, x_var = graph_multi[1][1], col_var = graph_multi[1][0])

