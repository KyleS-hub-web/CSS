# -*- coding: utf-8 -*-
"""
Data Pipeline for ETL

In this code-along, we'll focus on extracting data from flat-files. 
A flat file might be something like a .csv or a .json file. 
The two files that we'll be extracting data from are the apps_data.csv and 
the review_data.csv file. To do this, we'll used pandas. Let's take a closer look!

"""

import pandas as pd
import os
#%%

# Ingest these datasets into memory using read_csv and save as apps and reviews variable
apps = pd.read_csv('apps_data.csv')
reviews = pd.read_csv('review_data.csv')
#%%
# Take peak at the two data sets with print function or view in variable explorer



# View the columns, shape and data types of the data sets

# Is there a single pandas method that does this?

#print(apps.info())
"""
The code above works perfectly well, but this time let's try using DRY-principles to build a function to extract data.su

Create a function called extract, with a single parameter of name file_path.
Sprint the number of rows and columns in the DataFrame, as well as the data type of each column. Provide instructions about how to use the value that will eventually be returned by this function.
Return the variable data.
Call the extract function twice, once passing in the apps_data.csv file path, and another time with the review_data.csv file path. Output the first few rows of the apps_data DataFrame.

Extracting is one of the most tricky things to do in a data pipeline, always try to know much as you can about the source system, here its just a flat file which is quite simple.
"""

# Extract Function
def extract(file_path):
    # Read the file into memory
    data = pd.read_csv(file_path)
    # Now, print the details about the file
    print(data.info())
    # Print the type of each column

    # Finally, print a message before returning the DataFrame
    print("Data has been extracted successfully!")
    return data

# Call the function (create apps_data and reviews_data)

apps_data = extract('apps_data.csv')
reviews_data = extract('review_data.csv')

# Take a peek at one of the DataFrames


"""
We have extracted the data and now we want to transform them. 
Now we are going to use the food and drink category. 
So we are going to write a function that provides a top apps view for food and drink. 
So we will write a function that takes in 5 parameters, drop some duplicates
find positive reviews and filter columns. Then only keep a few columns. 
Then join it by min_rating and min_reviews, order it and check for min rating 
of 4 stars with at least 1000 reviews.

"""

#%%
catagories = apps_data['Category'].unique()


category = 'FOOD_AND_DRINK'
min_rating = 4
min_reviews = 1000

reviews_data = reviews_data.drop_duplicates()
apps_data = apps_data.drop_duplicates(subset=['App'])

subset_apps = apps_data[apps_data['Category'] == category]
print(subset_apps.head())

subset_reviews = reviews_data[reviews_data['App'].isin(subset_apps['App'])]

agg_reviews = subset_reviews.groupby('App')['Sentiment_Polarity'].mean().reset_index()

joined_app_reviews = subset_apps.merge(agg_reviews, on='App', how='left')

filtered_apps_reviews =  joined_app_reviews[['App', 'Reviews', 'Rating', 'Installs', 'Sentiment_Polarity']]

min_rating_apps = filtered_apps_reviews[filtered_apps_reviews['Rating'] >= min_rating]

top_apps = min_rating_apps[min_rating_apps['Reviews'].astype(int) >= min_reviews]

top_apps = top_apps.sort_values(by='Rating', ascending=False).fillna(0).reset_index(drop=True)
#%%
# Transform Function
def transform(apps,reviews,category, min_rating, min_reviews):
    # Print statement for observability
    print(f"Transforming data for {category} category...")

    #extract csv data
    apps_data = extract(apps)
    reviews_data = extract(reviews)


    # Drop any duplicates from both DataFrames (also have the option to do this in-place)
    reviews_data = reviews_data.drop_duplicates()
    apps_data = apps_data.drop_duplicates(subset=['App'])

    # Find all the apps and reviews in the food and drink category
    subset_apps = apps_data.loc[apps_data['Category'] == category]

    subset_reviews = reviews_data.loc[reviews_data['App'].isin(subset_apps['App'])]

    # Aggregate the subset_reviews DataFrame
    agg_reviews = subset_reviews.groupby('App')['Sentiment_Polarity'].mean().reset_index()

    # Join it back to the subset_apps table
    joined_app_reviews = subset_apps.merge(agg_reviews, on='App', how='left')

    # Keep only the needed columns
    filtered_apps_reviews = joined_app_reviews[['App',  'Rating','Reviews', 'Installs', 'Sentiment_Polarity']]
    # Convert reviews, keep only values with an average rating of at least 4 stars, and at least 1000 reviews
    filtered_apps_reviews.loc[:,'Reviews'] = filtered_apps_reviews['Reviews'].astype(int)
    min_rating_apps = filtered_apps_reviews[filtered_apps_reviews['Rating'] >= min_rating]

    top_apps = min_rating_apps.loc[min_rating_apps['Reviews'] >= min_reviews]
    # Sort the top apps, replace NaN with 0, reset the index (drop, inplace)
    top_apps = top_apps.sort_values(by=['Rating','Reviews'], ascending=[False,False]).fillna(0).reset_index(drop=True)
    # Persist this DataFrame as top_apps.csv file
    top_apps.to_csv('top_apps.csv', index=False)
    # Print what has happened so far
    print(f"Data has been transformed successfully for {category} category!")
    # Return the transformed DataFrame
    return top_apps
# Call the function
top_apps_data = transform('apps_data.csv','review_data.csv', 'FOOD_AND_DRINK', 4, 1000)


# Show the data





# Ok so last step is to load data, now you can save and keep it as csv but for it is
# a better practice to load it into sqlite DB or similar if its quite a large file.
# ...what advantages are there of loading into a SQL DB?

#%%
import sqlite3

# Load Function
def load(df, db_name, table_name):
    # Create a connection object
    con = sqlite3.connect(db_name)
    # Write the data to the specified table (table_name)
    df.to_sql(table_name, con, if_exists='replace', index=False)
    print(f"Data has been loaded to sqlite\n")
    # Read the data, and return the result (it is to be used)
    loaded_df = pd.read_sql(f"SELECT * FROM {table_name}", con)
    print('The loaded dataframe has been read from sqlite\n')
    # Add try/except to handle error handling and assert to check for conditions
    print(df.shape, loaded_df.shape)

    if (df.shape == loaded_df.shape):
        print("The shapes of the DataFrames match!")
    else:
        print("The shapes of the DataFrames do not match!")
# Call the function
load(df= top_apps_data, db_name='market_research.db', table_name='top_apps')
    
    
    
    
    
    