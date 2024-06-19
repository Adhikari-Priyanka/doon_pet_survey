import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import chi2


# Load csv file
cat = pd.read_csv("F:\\github\\doon_pet_survey\\cat_combine.csv")


# function that runs chisq for two pandas series

def run_chi2(df, s1, s2, alpha):
    c_tab = pd.crosstab(df[s1],df[s2]) # Create contingency table
    obs = c_tab.values # Observed values
    vals = stats.chi2_contingency(c_tab) # Run Chi2 test of independence of variables
    exp = vals[3] # Expected values
    
    norow = len(c_tab) # No of rows in c_tab
    nocol = len(c_tab.columns) # No of cols in c_tab
    dof = (norow-1) * (nocol-1) # Degree of freedom
    
    chi_sq = sum([(o-e)**2/e for o,e in zip(obs,exp)]).sum() # Find chi2 value
    crit = chi2.ppf(q = 1-alpha, df=dof) # Find critical value using alpha and degree of freedom
    
    pval = 1-chi2.cdf(x=chi_sq, df =dof)
    
    # Print results
    
    print('This chi2 test is run for columns : ',
          s1,' and ',s2)
    
    if chi_sq >= crit:
        print('reject h0, there is a relationship', '\n',
              'chi2 value = ', chi_sq, '\n',
              'critical value = ', crit, '\n')
    else:
        print('accept h0, there is no relationship', '\n',
              'chi2 value = ', chi_sq, '\n',
              'critical value = ', crit, '\n')
    if pval <= alpha:
        print('reject h0, there is a relationship', '\n',
              'p value = ', pval)
    else:
        print('accept h0, there is no relationship', '\n',
              'p value = ', pval)
    
    
run_chi2(df= cat, s1='cat_time_out', s2='cat_hunt_yn', alpha = 0.05)
