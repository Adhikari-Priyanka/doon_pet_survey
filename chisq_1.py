import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import chi2


# Load csv file
cat = pd.read_csv("F:\\github\\doon_pet_survey\\cat_combine.csv")


tab = pd.crosstab(cat['cat_time_out'], cat['cat_hunt_yn'])
obs = tab.values
val = stats.chi2_contingency(tab)
exp = val[3]

norow = len(tab.iloc[0:2,0])
nocol = len(tab.iloc[0,0:2])
dof = (norow-1) * (nocol-1)
alpha = 0.05

chi_sq = sum([(o-e)**2/e for o,e in zip(obs,exp)])
chi_sq_st = chi_sq[0]+chi_sq[1]

crit = chi2.ppf(q=1-alpha, df=dof)

pval = 1-chi2.cdf(x=chi_sq_st, df =dof)


if chi_sq_st >= crit:
    print('reject h0, there is a relationship \n pvalue is ',pval)
else:
    print('accept h0, there is no relationship \n pvalue is ',pval)