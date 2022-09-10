import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt

# This scrip will use the data from the csv file, and clean it. It will also show the avg temps per month and max aand minimum temp of the month
# Il will also plot 2 plots and save new csv files

directory_of_python_script = os.path.dirname(os.path.abspath(__file__))

# Transform from fahrenheit to celcius
def fahrenheit_to_celsius(col):
    Celsius = round((float(col) - 32) * 5.0/9.0, 1)
    return Celsius

# Replace date by month name
def month_name(col):
    date = datetime.strptime(col, "%d/%m/%Y").strftime('%b')
    return date

if __name__ == '__main__':

    df = pd.read_csv(os.path.join(directory_of_python_script, 'LEBZ_2021.csv'), sep=',')
    print(df.head())

    #  Rename the first column
    df.columns =['Date', 'Max of Day[ºC]', 'Avg of Day[ºC]', 'Min of Day[ºC]']

    # Show the temp in celcius
    for col in df:
        if col == 'Date':
            continue
        df[col] = df[col].apply(fahrenheit_to_celsius)

    df.to_csv(os.path.join(directory_of_python_script, 'LEBZ_2021_Clean.csv'))

    # Replace the date by month names
    df['Date'] = df['Date'].apply(month_name)
    df.rename(columns = {'Date':'Month'}, inplace = True)

    df.plot.line(x='Month', y=['Max of Day[ºC]', 'Avg of Day[ºC]', 'Min of Day[ºC]'], color = ['#FF1600','#FADC00','#01E6FA'], 
                              title = 'Temperatures over the year for each day', label=['Max of Day', 'Avg of Day', 'Min of Day'])
    plt.xlabel('Days')
    plt.ylabel('Temperature[ºC]')
    plt.show()

    # Get avg max, min and avg temperature of the month
    avg_df = round(df.groupby('Month', sort=False, as_index=False).mean(),1)
    avg_df.rename(columns = {'Max of Day[ºC]':'Avg Max of Month[ºC]','Avg of Day[ºC]':'Avg of Month[ºC]', 'Min of Day[ºC]':'Avg Min of Month[ºC]'}, inplace = True)
    
    # Get the max and min temp of the month
    max = df.groupby('Month', sort=False, as_index=False)['Max of Day[ºC]'].max()
    min = df.groupby('Month', sort=False, as_index=False)['Min of Day[ºC]'].min()
    max.drop('Month',axis=1, inplace=True)
    min.drop('Month',axis=1, inplace=True)

    avg_df = pd.concat([avg_df, max, min], axis=1)
    avg_df.rename(columns = {'Max of Day[ºC]':'Max of Month[ºC]', 'Min of Day[ºC]':'Min of Month[ºC]'}, inplace = True)
    avg_df.to_csv(os.path.join(directory_of_python_script, 'LEBZ_2021_Month.csv'))
    
    plt.plot(avg_df['Month'], avg_df['Avg Max of Month[ºC]'], marker = 'o', color = '#FF1600', label = 'Avg Max of Month')
    plt.plot(avg_df['Month'], avg_df['Avg of Month[ºC]'], marker = 'o', color = '#FADC00', label = 'Avg of Month')
    plt.plot(avg_df['Month'], avg_df['Avg Min of Month[ºC]'], marker = 'o', color = '#01E6FA', label = 'Avg Min of Month')
    plt.legend()
    plt.xlabel('Month')
    plt.ylabel('Temperature[ºC]')
    plt.title('Average temperature per month')
    plt.show()