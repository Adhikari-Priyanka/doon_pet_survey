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

col_scale = ['#999999','#566455', '#765387']

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
    return f'{chi_sq_result} Chi square value = {chi_sq} and Critical value = {crit} at alpha={alpha} and df={dof} {pval_result} as P value = {pval}\n'


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
    return f'{chi_sq_result} Chi square value = {chi_sq} and Critical value = {crit} at alpha={alpha} and df={dof} {pval_result} as P value = {pval}\n'


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
