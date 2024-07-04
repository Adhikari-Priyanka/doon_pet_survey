import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import chi2
import os

## Change file path as needed!!!!
wd = 'F:\\github\\doon_pet_survey_graphs\\chi2_tests\\'

# Load csv file
cat = pd.read_csv("F:\\github\\doon_pet_survey_graphs\\cat_combine.csv")
dog = pd.read_csv("F:\\github\\doon_pet_survey_graphs\\dog_combine.csv")

# Define independent and dependent variables (single option columns ONLY)
cat_dep_var = ['cat_hunt_yn', 'cat_hunt_freq']
cat_indep_var = ['cat_sex','cat_neutered','cat_describe',
             'cat_age','cat_time',
             'cat_time_out','cat_stay',
             'cat_feed_freq']

dog_dep_var = ['dog_hunt_yn','dog_hunt_freq']
dog_indep_var = ['dog_neutered', 'dog_sex', 'dog_age']


# Define a function that runs chisq for two pandas series

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


# Run the chi square test for all combinations of dependent and independent variables
# And save as a text file

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

# Save contingency table as text file

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
            res = pd.crosstab(cat[dv],cat[iv]) 
            f.write(f'CAT Contingency table for {dv} and {iv}: \n{res}\n\n')
    for dv in dog_dep_var:
        for iv in dog_indep_var:
            res = pd.crosstab(dog[dv],dog[iv])
            f.write(f'DOG Contingency table for {dv} and {iv}: \n{res}\n\n')



