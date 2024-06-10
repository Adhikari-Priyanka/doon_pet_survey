import pandas as pd
import numpy as np


# Load MASTERSHEET

df = pd.read_csv("F:\\github\\doon_pet_survey\\MASTERSHEET.csv")
print('no of rows in dataframe is', len(df))

## add an index column (to offset for column numbers as per excel)
df.insert(loc=0, column='index', value=range(len(df)))

## filter by column 'consent' == 'Yes'
df1 = df.loc[df["consent"] == 'Yes']
print('no of responses with consent is', len(df1))

## filter by column 'have_pets' != 'No'
df2 = df1.loc[df["have_pets"] != 'No']
print('no of responses with pets is',len(df2))

# Cats dataframe
## filter by column 'kind_of_pets' != 'Dog(s)'
cats = df2.loc[df["kind_of_pets"]!='Dog(s)']
print('no of responses with cats or cats and dogs both is',len(cats))

# Dogs ONLY dataframe
## filter by column 'kind_of_pets' != 'Cat(s)'
dogs = df2.loc[df["kind_of_pets"]!='Cat(s)']
print('no of responses with dogs or cats and dogs both is',len(dogs))


# create the following combine columns:

## cat_age
## cat_sex
## cat_neutered
## cat_feed
## cat_feed_freq
## cat_time_out
## cat_stay
## cat_hunt
## cat_hunt_freq
## cat_time

# Function to combine columns based on column suffix 
# (for suffix 'age' and pet 'cat', combines cat1_age, cat2_age, cat3_age, cat4_age,cat5_age into single pandas series)

def col_combin1 (df, col_suffix, pet):
    # df: Enter name of the dataframe
    # col_suffix: Enter the suffix of the column to combine
    # pet: Enter which pet - dog or cat 
    
    col_filter1 = df.filter(like = col_suffix)
    col_filter2 = col_filter1.filter(like = pet)
    
    col_to_drop = col_filter2.columns[col_filter2.columns.str.contains('comment')]
    col_filter3 = col_filter2.drop(col_to_drop, axis=1)
    
    columns_to_concat = [col_filter3[col] for col in col_filter3.columns]
    result = pd.concat(columns_to_concat, axis=0)
    return result

age = col_combin1(cats, 'age', 'cat')
print(type(age))
print(len(age))


# Function to create a dataframe of all combined column characteristics

columns_list = ['age', 'sex', 'neutered', 'feed', 'feed_freq', 
                'time_out', 'stay', 'hunt', 'hunt_freq', 'time']

def col_combin2 (df, col_suffix_list, pet):
    # df: Enter name of the dataframe
    # col_suffix_list: Enter the suffix of the column to combine
    # pet: Enter which pet - dog or cat 
    
    #Filter by type of pet
    col_filter1 = df.filter(like = pet)
    
    #Drop comment columns
    col_to_drop = col_filter1.columns[col_filter1.columns.str.contains('comment')]
    col_filter2 = col_filter1.drop(col_to_drop,axis =1)
    
    #define empty list
    result = []
    result = df['row_ids']
    
    #filter by col_suffix_list
    for i in col_suffix_list:
        col_filter3 = col_filter2.filter(like = i)
        columns_to_concat = [col_filter3[col] for col in col_filter3.columns]
        concat_column = pd.concat(columns_to_concat, axis=0)
        result = pd.concat([result, concat_column] ,axis =1)
        
    return result

col_combin2(cats, columns_list, 'cat')



####### raise ValueError("cannot reindex on an axis with duplicate labels")