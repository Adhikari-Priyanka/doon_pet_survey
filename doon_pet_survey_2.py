import pandas as pd
import numpy as np


# Load MASTERSHEET
df1 = pd.read_csv("F:\\github\\doon_pet_survey\\MASTERSHEET.csv")
print('No of responses is ', len(df1))

# Remove columns not required for further analysis
## Remove columns with comments
comment_col = df1.columns.str.contains('comment')
print( 'Removing columns containing comments only - ', df1.columns[comment_col])
df1 = df1.drop(df1.columns[comment_col] , axis=1)

## Remove columns with survey response data (start time, date etc)
response_col = ['start_time','completion_time', 'email_id' , 'name' ,'last_modified']
print('Removing columns with survey response data - ', response_col)
df2 = df1.drop( response_col , axis =1)

## Remove columns with survey respondent data (Name, address etc)
respondent_col = ['full_name' ,'gender' ,'city', 'address',
                  'postcode', 'phone', 'email', 'longterm']
print('Removing columns with survey respondent data - ', respondent_col)
df3 = df2.drop( respondent_col , axis =1)

print('Remaining columns in dataframe - ', df3.columns)

# Filter by consent and have_pets columns
## filter by column 'consent' == 'Yes'
df4 = df3.loc[df3["consent"] == 'Yes']
print('No of responses with consent is', len(df4))

## filter by column 'have_pets' != 'No'
df5 = df4.loc[df4["have_pets"] != 'No']
print('No of responses with pets is',len(df5))

# # Remove unused variables
del (df1,df2, df3, df4)

#########################################################################

# Create pet dataframes

## Remove 'consent' and 'have_pets' columns
col_drop1 = ['consent', 'have_pets']
df6 = df5.drop(col_drop1, axis = 1)

# Cats dataframe
## filter by column 'kind_of_pets' to include both 'Cat(s)' and 'Both'
cats1 = df6.loc[df6["kind_of_pets"]!='Dog(s)']
## drop columns with dog prefix and 'kind of pets'
dog_col = df6.columns.str.contains('dog')
cats2 = cats1.drop(df6.columns[dog_col] , axis = 1)
## Remove column 'kind_of_pets'
cats = cats2.drop('kind_of_pets' , axis=1)

# Dogs dataframe
## filter by column 'kind_of_pets' to include both 'Dog(s)' and 'Both'
dogs1 = df6.loc[df6["kind_of_pets"]!='Cat(s)']
## drop columns with dog prefix and 'kind of pets'
cat_col = df6.columns.str.contains('cat')
dogs2 = dogs1.drop(df6.columns[cat_col] , axis = 1)
## Remove column 'kind_of_pets' 'have_dogs', 'no_dogs'
dogs = dogs2.drop(['kind_of_pets', 'have_dogs', 'no_dogs'] , axis=1)


print('No of response with cats or both is ', len(cats))
print('No of response with dogs or both is ', len(dogs))
print('columns in the cat dataframe - ' , cats.columns)
print('columns in the dog dataframe - ' , dogs.columns)

# Remove unused variables
del(cats1, cats2, dogs1, dogs2)


######################################################################


# write a function that makes dataframes for columns with suffic _n
# where n is 1 - 5

def col_combin(df):
    # df is either dogs or cats
    
    # Dataframe of columns with suffix 1
    pet1_drop = df.columns.str.contains('2|3|4|5')
    pet1 = df.drop(df.columns[pet1_drop] , axis=1)
    print('no row pet1 - ', len(pet1))
    print('columns _1 - ', pet1.columns)
    
    # Dataframe of columns with suffix 2
    pet2_drop = df.columns.str.contains('1|3|4|5')
    pet2 = df.drop(df.columns[pet2_drop] , axis=1)
    print('no row pet2 - ', len(pet2))
    print('columns _2 - ', pet2.columns)    
    
    # Dataframe of columns with suffix 3
    pet3_drop = df.columns.str.contains('1|2|4|5')
    pet3 = df.drop(df.columns[pet3_drop] , axis=1)
    print('no row pet3 - ', len(pet3))    
    print('columns _3 - ', pet3.columns) 
    
    # Dataframe of columns with suffix 4
    pet4_drop = df.columns.str.contains('1|3|2|5')
    pet4 = df.drop(df.columns[pet4_drop] , axis=1)
    print('no row pet4 - ', len(pet4))   
    print('columns _4 - ', pet4.columns)  
    
    # Dataframe of columns with suffix 5
    pet5_drop = df.columns.str.contains('1|3|4|2')
    pet5 = df.drop(df.columns[pet5_drop] , axis=1)
    print('no row pet5 - ', len(pet5))    
    print('columns _5 - ', pet5.columns)   
    
    # Combine dataframes into one rowwise
    pet_combin = pd.DataFrame(np.concatenate( (pet1.values, pet2.values, pet3.values, pet4.values, pet5.values) , axis=0))
    print('no row pet_combin ', len(pet_combin))
    
    # Give column names to combined dataframe
    col_names = [name.replace('1', '') for name in pet1.columns]
    pet_combin.columns = col_names
    
    # Return combined dataframe
    return pet_combin

# Run the function for cats and dogs
print('Running function to combine cats dataframe')
cat_result = col_combin(cats)

print('Running function to combine dogs dataframe')
dog_result = col_combin(dogs)

# Export combined dataframe as csv
cat_result.to_csv('cat_combine.csv', sep=',')
dog_result.to_csv('dog_combine.csv', sep=',')

# Remove NA values
cat_result_nona = cat_result.dropna(subset=['cat_age'])
print('length of cleaned df ',len(cat_result_nona))
print('length of non na values in cat_age' , 
      len(cat_result[~cat_result['cat_age'].isnull()]))

dog_result_nona = dog_result.dropna(subset=['dog_age'])
print('length of cleaned df ',len(dog_result_nona))
print('length of non na values in dog_age' , 
      len(dog_result[~dog_result['dog_age'].isnull()]))

# Export combined dataframe as csv
cat_result_nona.to_csv('cat_combine_nona.csv', sep=',')
dog_result_nona.to_csv('dog_combine_nona.csv', sep=',')


