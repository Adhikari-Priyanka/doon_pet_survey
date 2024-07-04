import pandas as pd
import numpy as np
import os
import plotly.express as px
import kaleido
import plotly.io as pio

## Change file path as needed!!!!
wd = 'F:\\github\\doon_pet_survey_graphs\\'

# Load MASTERSHEET
df1 = pd.read_csv(f'{wd}MASTERSHEET.csv')
print('No of responses is ', len(df1))

# 1. Remove columns not required for further analysis
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
df5 = df4.loc[df4["have_pets"] == 'Yes']
print('No of responses with pets is',len(df5))

# # Remove unused variables
del (df1,df2, df3, df4)

#########################################################################

# 2. Create pet dataframes

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

## Write a function that makes dataframes for columns with suffic _n
## where n is 1 to 5

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
cat_result.to_csv(f'{wd}cat_combine.csv', sep=',')
dog_result.to_csv(f'{wd}dog_combine.csv', sep=',')

# Remove unused variables
del(cat_result,dog_result, cats, dogs)

#########################################################################

# 3. Generate a txt file with summary stats for all columns

## Load csv files for cat and dog
cat = pd.read_csv(f'{wd}cat_combine.csv')
dog = pd.read_csv(f'{wd}dog_combine.csv')

## Define a dictionary with customized order of values in columns
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
dog_order_dict = {
    'dog_age' : ['0-3 months', '3 months - 1 year','1-3 years','3-5 years','5-8 years','8 - 12 years','12 years and older'],
    'dog_sex' : ['Female', 'Male'],
    'dog_neutered' : ['Neutered', 'Not neutered'],
    'dog_hunt_yn' : ['Yes', 'No', 'Have not observed'],
    'dog_hunt_freq' : ['Once every few months','Once a month','Once in 15 days','Once a week','Everyday']
}

## Save frequency tables as text file

filename = f'{wd}Frequency tables.txt'
if not os.path.isfile(filename):
    # If the file does not exist, create it
    with open(filename, 'w') as file:
        file.write('')  # Create an empty file
    print(f"'{filename}' has been created.")
else:
    print(f"'{filename}' already exists.")

with open(filename,'w') as f: # Open the file
    # For cat single option variables (cat1 to cat5)
    remove = ['row_ids', 'Unnamed: 0', # Dont need frequency table for index
              'cat_hunt_yn', 'cat_describe', # Not corresponding to individual cat
              'cat_feed', 'cat_hunt' # Contains multiple options in one
              ]
    for col in cat.columns.drop(remove): 
        res = cat[col].value_counts().reindex(cat_order_dict[col]) # Count values in col and reorder based on dict
        res_count = len(cat[col].dropna()) # Count total number of cats
        f.write(f' CAT frequency table for {col}: \n{res}\n Total cats = {res_count}\n\n\n')
        
    # For cat multiple option variables (cat1 to cat5)
    multi = ['cat_hunt', 'cat_feed']
    for col in multi:
        fix = cat[col].str.split(';').explode().reset_index(drop=True)
        fix1 = fix.dropna() # Remove NA values
        fix2 = fix1[fix1!=''] # Remove blank values
        fix3 = fix2.str.split('(').str.get(0).str.strip() # Remove text inside ()
        res = fix3.value_counts()
        res_count = len(cat[col].dropna()) # Count total number of cats
        f.write(f' CAT frequency table for multiple option column: {col}: \n{res}\n Total cats = {res_count}\n\n\n')

    # For dog single option variables (dog1 to dog5)
    remove = ['row_ids', 'Unnamed: 0', # Dont need frequency table for index
              'dog_hunt' # Contains multiple options in one
              ]
    for col in dog.columns.drop(remove): 
        res = dog[col].value_counts().reindex(dog_order_dict[col]) # Count values in col and reorder based on dict
        res_count = len(dog[col].dropna()) # Count total number of dogs
        f.write(f' DOG frequency table for {col}: \n{res}\n Total dogs = {res_count}\n\n\n')

    # For dog multiple option variables (dog1 to dog5)
    multi = ['dog_hunt']
    for col in multi:
        fix = dog[col].str.split(';').explode().reset_index(drop=True)
        fix1 = fix.dropna() # Remove NA values
        fix2 = fix1[fix1!=''] # Remove blank values
        fix3 = fix2.str.split('(').str.get(0).str.strip() # Remove text inside ()
        res = fix3.value_counts()
        res_count = len(dog[col].dropna()) # Count total number of dogs
        f.write(f' DOG frequency table for multiple option column: {col}: \n{res}\n Total dogs = {res_count}\n\n\n')

#########################################################################

# 4.1 Generate histograms for each single option column in cat and dog 

## Create folder to store histograms
filepath = f'{wd}\\histograms\\'
if not os.path.exists(filepath):
    os.makedirs(filepath)

## Function to generate histograms

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
    pio.write_image(fig, f'{filepath}hist_{var}.png', engine="kaleido")
    
    # Display success message
    print('Prepared histogram for ', var)


## Make histograms for each column in cat.csv
for col_name in cat.columns[2:]:
    try:
        print('graph for ', col_name)
        histo(df=cat, var=col_name, order_dict=cat_order_dict)
    except:
        print('could not make graph for ', col_name)
        pass

## Make histograms for each column in dog.csv
for col_name in dog.columns[2:]:
    try:
        print('graph for ', col_name)
        histo(df=dog, var=col_name, order_dict=dog_order_dict)
    except:
        print('could not make graph for ', col_name)
        pass

#########################################################################

# 4.2 Generate histograms for each multiple option column in cat and dog 

## Create folder to store histograms
filepath = f'{wd}\\histograms\\multi\\'
if not os.path.exists(filepath):
    os.makedirs(filepath)

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
    pio.write_image(fig, f'{filepath}hist_{var}.png', engine="kaleido")
    
    # Display success message
    print('Prepared histogram for ', var)

# Create histograms
histo_multi(cat, 'cat_hunt')
histo_multi(cat,'cat_feed')
histo_multi(dog,'dog_hunt')

