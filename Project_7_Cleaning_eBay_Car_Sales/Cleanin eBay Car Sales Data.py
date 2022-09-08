from datetime import datetime
import pandas as pd
import numpy as np
import re
import os
pd.options.mode.chained_assignment = None

directory_of_python_script = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(directory_of_python_script, 'autos.csv'), sep=',', encoding = 'Latin-1')

# Clean column names
def clean_col(col):
    return re.sub(r"([A-Z])", r" \1", col).strip().replace(' ','_').lower()

# Clean dates
def clean_dates(column):
    date = column[:10].split('-')
    date = '/'.join(i for i in reversed(date))
    date = datetime.strptime(date, "%d/%m/%Y").strftime("%d/%m/%Y")
    return date

def clean_price(column):
    if pd.isnull(column) == True:
        return None
    price = column.replace('$','').replace(',','')
    return int(price)
def clean_odometer(column):
    if pd.isnull(column) == True:
        return None
    odometer = column.replace('km','').replace(',','')
    return int(odometer)

def clean_range(column):
    if pd.isnull(column) == True:
        return None
    range = str(column).replace('(','').replace(']','').replace(',',' -')
    return range
if __name__ == "__main__":

    df.columns=[clean_col(col) for col in df.columns]

    # Delete all rows with any value NAN
    #df.dropna(inplace=True)

    # Drop columns cause they have no useful information or very few information
    df.drop(['nr_of_pictures', 'offer_type', 'seller'], axis=1, inplace=True)

    # Update date to date type and clean it
    for col in df.columns:
        if 'date' in col or 'seen' in col:
            dates = df[col].apply(clean_dates)
            df[col] = dates

    # Clean month of registation and year of registation because they have impossible values
    df = df[df['month_of_registration'] > 0]

    # After testing fount out that 96% of the cars were registraed between 1900 and 2016
    df['year_of_registration'].between(1900,2016).sum()/df.shape[0]
    df = df[df['year_of_registration'].between(1900,2016)]

    # Put price as an integer to evaluate better
    df['price'] = df['price'].apply(clean_price)
    df = df.rename(columns={'price':'price_dollars'})

    # Check prices
    df['price_dollars'].describe()
    df['price_dollars'].sort_values(ascending=False).head(15) # Prices above 350000 are unrealistic and seem like a joke
    df['price_dollars'].sort_values(ascending=True).head(15) # Prices of 0 are unrealistic, since it is eBay price of 1 is possible
    df = df[df['price_dollars'].between(1,350000)]

    # Put km as an integer to evaluate better
    df['odometer'] = df['odometer'].apply(clean_odometer)
    df = df.rename(columns={'odometer':'odometer_km'}) 

    # Check km
    df['odometer_km'].describe() # After evaluating there arent any extreme high values or low values
    
    # Get mean price by km range
    odometer_range = df[['price_dollars']]
    odometer_range['range_of_km'] = pd.cut(df['odometer_km'], 5, include_lowest=True)
    odometer_range['range_of_km'] = odometer_range['range_of_km'].apply(clean_range)
    print(odometer_range.groupby('range_of_km').mean().round()) # The lower the km the higher the price
    
    # Get the mean price of most popular brands
    df['brand'].value_counts(normalize=True) * 100 # There are only 6 brands that make more than 5% of sales
    brands = df['brand'].value_counts(normalize=True)

    # Select those brands
    top_brands = brands[brands > 0.05].index

    # Save the brands and mean price in a dict
    brand_mean_price = {}
    for brand in top_brands:
        only_top_brands = df[df['brand']==brand]
        mean_price = int(only_top_brands['price_dollars'].mean())
        brand_mean_price[brand] = mean_price
    print(brand_mean_price)

    # Change the german words to english words
    df['gearbox'] = df['gearbox'].replace(['manuell', 'automatik'],['manual','automatic'])
    print(df['gearbox'].value_counts())
    df['not_repaired_damage'] = df['not_repaired_damage'].replace(['nein','ja'],['no','yes'])
    print(df['not_repaired_damage'].value_counts())
    df['fuel_type'] = df['fuel_type'].replace(['benzin', 'elektro', 'andere'], ['gasoline', 'electric', 'other'])
    print(df['fuel_type'].value_counts())
    df['vehicle_type'] = df['vehicle_type'].replace(['limousine', 'kleinwagen', 'kombi','bus','cabrio','coupe','suv','andere'], 
                           ['sedan', 'small car', 'station wagon', 'bus', 'convertible', 'coupe','suv','other'])
    print(df['vehicle_type'].value_counts())
    df['model'] = df['model'].replace('andere', 'other')
    df.to_csv(os.path.join(directory_of_python_script, 'autos_clean.csv'), index=False)

    # See mean price id car has damage or not
    print(df.groupby('not_repaired_damage')['price_dollars'].mean().round())