from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the data set
directory_of_python_script = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(directory_of_python_script,'euro-daily-hist_1999_2022.csv'))

df.rename(columns={'Period\\Unit:':'Time'}, inplace = True)

# Get the main currencies
df = df[['Time', '[Brazilian real ]', '[Swiss franc ]', 
              '[Indian rupee ]', '[Japanese yen ]', '[Korean won ]', '[Mexican peso ]',
              '[Norwegian krone ]', '[Russian rouble ]', '[Swedish krona ]', 
              '[US dollar ]', '[South African rand ]', '[UK pound sterling ]']]

# Cleaning the data frame
df.reset_index(drop=True, inplace=True)
main_df = df.copy()

for name in main_df.columns:

    # Delete all the rows with -, converting all the values to floats, and making the name columns more legible
    if name == 'Time':
        continue
    main_df=main_df[main_df[name] != '-']
    main_df = main_df.astype({name:float})
    upd_name = name.replace('[','').replace(' ]','').replace(' ','_')
    main_df.rename(columns={name:name.replace('[','').replace(' ]','').replace(' ','_')}, inplace=True)

# Setting the time as type time
main_df['Time'] = pd.to_datetime(main_df['Time'])
main_df.sort_values('Time', inplace=True)

# Getting only the values from 2000
main_df = main_df[main_df['Time'] > datetime(1999,12,31)]
main_df.reset_index(drop=True, inplace=True)

# Eliminating all nan
main_df.dropna(inplace=True)

# Visualising data
currencies = main_df.drop('Time', axis=1).columns.to_list()
c=0
figure, axs = plt.subplots(4,3,sharex=True)
for i in range(4):
    for j in range(3):
        axs[i,j].plot(main_df["Time"], main_df[currencies[c]])
        axs[i,j].set_title('Euro to ' + currencies[c], fontsize = 10)
        c = c+1
plt.show()
