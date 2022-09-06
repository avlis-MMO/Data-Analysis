from cmath import pi
from turtle import color
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import os

# Path to get and save info, same place as code
directory_of_python_script = os.path.dirname(os.path.abspath(__file__))

# Function to create the pie chart
def Get_Nat(Places):

    # Get the percentage to use in the legend
    total = Places['Born in'].str[-1].value_counts().values.sum()
    percent = Places['Born in'].str[-1].value_counts().values * 100 / total
    data = []
    other = 'Other:\n'
    labels = []
    i = 0

    # Create the labels of the legend
    # Since there were a lot of cuntries where they have only one person all of them were put together in other category
    for p,c,n in zip(percent,Places['Born in'].str[-1].value_counts().index.to_list(),Places['Born in'].str[-1].value_counts().values):
        
        # The criteria to select wich countries goes to the other category is to have less than 1% of the 500
        if p>1:
            data.append(n)
            labels.append('{0}({1}) - {2:1.1f} %'.format(c,n,p))
        else:
            # This was done to format the box containinf the explanatory text
            i = i +1
            if i == 4:
                other= other + ' {0}({1})\n'.format(c,n)
                i = 0
            else:
                other= other + ' {0}({1}),'.format(c,n)

    # Get the number of people in the other category            
    data.append(total-sum(data))
    labels.append('Other')
    colors = sns.color_palette('pastel')[0:len(labels)]

    # Create the fig and axis, 2 axis were create to have a better legend and an explanatory text
    fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2, 1]})
    fig.suptitle('Nationality of the top 500 actors/actresses')

    # Create the donut pie chart
    pie = ax1.pie(data, autopct='%1.1f%%', colors = colors, startangle=0, pctdistance=1.2, wedgeprops=dict(width=0.4, edgecolor='white'))
    ax2.axis('off')
    legend = ax2.legend(pie[0], labels, fontsize = 10, loc='center', bbox_to_anchor=(0.5, 0.63), ncol=2)
    frame = legend.get_frame()
    frame.set_edgecolor((1,1,1,0))
    ax2.text(-0.06,0.28,other)

    # Create a square to make the legend and text more appealing and organized
    rect = patches.Rectangle((-0.05, 0.22), 1.3, 0.55, linewidth=3, edgecolor='grey', facecolor='none')
    plt.gca().add_patch(rect)
    file_name = 'Nat.png'
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(16, 7) # set figure's size manually to ht best possible (16x7)
    plt.savefig(os.path.join(directory_of_python_script, file_name), bbox_inches='tight', dpi=300)
    plt.show()

# Function to create the pie chart and histograms
def Get_Gender_Age(Genders, Age, Avg_age):

    # Create a fig with 3 slots in one on the left two on the right
    fig = plt.figure()
    ax11 = fig.add_subplot(121)
    ax12 = fig.add_subplot(222)  
    ax13 = fig.add_subplot(224)
    Labels = []

    # Get labels and colors right, cause depending on the dataset the position 0 for the index may change
    for g in Genders.index:
        Labels.append('Male' if g == 'M' else 'Female')
    if Genders.index[0] == 'M':
        colors = ['skyblue','pink']
    else:
        colors = ['pink','skyblue']
    
    # Create the pie chart
    ax11.pie(Genders, autopct='%1.1f%%', startangle=0, pctdistance=0.8, wedgeprops=dict(width=0.4, edgecolor='white'), colors=colors)
    ax11.legend(Labels, loc = 'center', bbox_to_anchor=(0.5,0.5))
    ax11.set_title("Percentage of Male and Female in the top 500")

    # Create both histograms with all the details in palce
    ax12.hist(Age[0], color = 'skyblue', alpha=0.5, histtype='bar', ec='white')
    # Create a line with the average age
    ax12.axvline(Avg_age[0], color ='black', linestyle='dashed',label='Avg_age[0]')
    trans = ax12.get_xaxis_transform()
    ax12.text(Avg_age[0], .80, ' Avg. Age {0}'.format(Avg_age[0]), transform=trans)
    ax12.set_title("Male Age")
    ax12.set_xlabel('Years')
    ax12.set_ylabel('Nº', rotation=0)
    ax12.xaxis.set_label_coords(1, -0.025)
    ax12.yaxis.set_label_coords(-0.03, 1.03)
    ax13.hist(Age[1], color = 'pink', alpha=0.5, histtype='bar', ec='white')
    # Create a line with the average age
    ax13.axvline(Avg_age[1], color ='black', linestyle='dashed',label='Avg_age[0]')
    trans = ax13.get_xaxis_transform()
    ax13.text(Avg_age[1], .80, ' Avg. Age {0}'.format(Avg_age[1]), transform=trans)
    ax13.set_title("Female Age")
    ax13.set_xlabel('Years')
    ax13.set_ylabel('Nº', rotation=0)
    ax13.xaxis.set_label_coords(1, -0.025)
    ax13.yaxis.set_label_coords(-0.03, 1)
    file_name = 'Gender_Age.png'
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(16, 7) # set figure's size manually to ht best possible (16x7)
    plt.savefig(os.path.join(directory_of_python_script, file_name), bbox_inches='tight', dpi=300)
    plt.show()

# Function to create the nested pie chart
def Movies(movies):

    size = 0.3
    inner_labels = []
    pct = []
    pct_all = []
    fig, ax = plt.subplots()
    ax.axis('equal')

    # Get the outer values, movies separated by age
    outer = movies.groupby(['Gender'])['Movies/Series'].sum()
    # Get the inner values, movies separated by age and then by age gap
    inner = movies.groupby(['Gender','Age Gap'])['Movies/Series'].sum()

    # Get the percentage of the inner sections for male and female
    pct_m = np.round_(inner['M'].values *100 / inner['M'].values.sum(), decimals=1)
    pct_f = np.round_(inner['F'].values *100 / inner['F'].values.sum(), decimals=1)
    
    # Set the colors and labels of the outer pie according to the index
    if outer.index[0] == 'M':
        colors = ['skyblue','pink']
        outer_labels = ['Male', 'Female']

        # Save all the percentages in a list and the percentages higher than 5% in another, this ones will be used to put 
        # on the inner pie so that is why it has to be higher than 5% to look good, and they are add to the list depending on
        # the index
        for i in pct_m:
            pct_all.append(i)
            if i > 5:
                pct.append(i)
            else:
                pct.append('')
        for i in pct_f:
            pct_all.append(i)
            if i > 5:
                pct.append(i)
            else:
                pct.append('')
    else:
        colors = ['pink','skyblue']
        outer_labels = ['Female', 'Male']
        for i in pct_f:
            pct_all.append(str(i)+'%')
            if i > 5:
                pct.append(str(i)+'%')
            else:
                pct.append('')
        for i in pct_m:
            pct_all.append(str(i)+'%')
            if i > 5:
                pct.append(str(i)+'%')
            else:
                pct.append('')

    # Get the size of the values to create the colors for the handles
    m_size = len(inner['M'].values)
    f_size = len(inner['F'].values)

    # Get colors maps
    cmap1 = plt.cm.Blues
    cmap2 = plt.cm.RdPu
    
    labels1 = inner.index.get_level_values(1)

    # Get inner labels for the handles
    for i,j in zip((pct_all), (labels1)):
        inner_labels.append('{0} ({1})'.format(j,i))

    # Get the inner colors for the handles
    if outer.index[0] == 'M':
        inner_colors = [*cmap1(np.linspace(1, .1, m_size)), *cmap2(np.linspace(1, .1, f_size))]
    else:
        inner_colors = [*cmap2(np.linspace(1, .1, f_size)), *cmap1(np.linspace(1, .1, m_size))]
    
    pie1 = ax.pie(outer.values.flatten(), radius=1, colors=colors, labels= outer_labels,
        autopct='%1.1f%%', pctdistance=0.85, wedgeprops=dict(width=size, edgecolor='w'))

    pie2 = ax.pie(inner.values.flatten(), radius=1-size, colors=inner_colors, labels=pct,
        labeldistance=0.75, textprops = dict(ha='center'), wedgeprops=dict(width=size, edgecolor='w'))
    
    # pie[0] to get only the handles of the inner pie
    ax.legend(pie2[0], inner_labels, loc=(0.9, 0.17))
    ax.set(aspect="equal", title='Number of movies made by top 500 by gender and age gap')
    ax.text(2.015,-0.9,('Total nº of movies: {0}'.format(outer.sum())))
    file_name = 'Movies.png'
    figure = plt.gcf()
    figure.set_size_inches(14, 7)
    plt.savefig(os.path.join(directory_of_python_script, file_name), bbox_inches='tight', dpi=300)
    plt.show()   

if __name__ == "__main__":
    
    # Open file saved from previous script
    df = pd.read_csv(os.path.join(directory_of_python_script, 'IDMb.csv'), sep=',')
    del df['Unnamed: 0']
    
    Alive = df.loc[df['Death'] == 'Alive'].shape[0]
    # Create pie chart with female and male percentage and histograms with age distributions
    # Get list of list with the male and female age separate and assing position 0 to male and 1 to female
    Age = [df.loc[df['Gender'] == i]['Age'].to_list() for i in ['M','F']]

    # Get average age of female and male and assing position 0 to male and 1 to  female
    Avg_Ages = df.groupby(['Gender'])['Age'].mean()
    List_avg_age = [[round(Avg_Ages.values[0]), round(Avg_Ages.values[1])] if Avg_Ages.index[0] == 'M' else [round(Avg_Ages.values[1]), round(Avg_Ages.values[0])]]
   
    # Call function to draw the graphs
    Get_Gender_Age(df['Gender'].value_counts(), Age, List_avg_age[0])

    # Create nested pie chart with the movies grouped by gender and age gap
    selected_rows = df[~df['Age'].isnull()]
    age_gap=[]
    for i in selected_rows['Age']:
        if 0<=i<10:
            age_gap.append('0 - 10')
        if 10<=i<20:
            age_gap.append('10 - 20')
        if 20<=i<30:
            age_gap.append('20 - 30')
        if 30<=i<40:
            age_gap.append('30 - 40')
        if 40<=i<50:
            age_gap.append('40 - 50')
        if 50<=i<60:
            age_gap.append('50 - 60')
        if 60<=i<70:
            age_gap.append('60 - 70')
        if 70<=i<80:
            age_gap.append('70 - 80')
        if 80<=i<90:
            age_gap.append('80 - 90')
        if 90<=i<100:
            age_gap.append('90 - 100')

    selected_rows['Age Gap'] = age_gap
    Movies(selected_rows)
    
    # Create pie chart with the distribution of the nationalities
    # Get only the column with the informatin about the country they were born and create a dataframe with that info only
    Places = df[df['Born in'].notna()]['Born in'].str.replace(', ',',').str.split(',').reset_index()
    del Places['index']

    # Clean and tidy the data
    for ind, row in enumerate(Places['Born in']):

        if row[-1] == 'USSR [now Ukraine]':
            row[-1] = 'Ukraine'

        if row[-1] == 'USSR [now Armenia]':
            row[-1] = 'Armenia'

        if row[-1] == 'United Kingdom':
            row[-1] = 'UK'

        if row[-1] == 'England':
            row[-1] = 'UK'
        
        if row[-1] == 'United States':
            row[-1] = 'USA'
        
        if row[-1] == 'West Germany':
            row[-1] = 'Germany'
        
        if row[-1] == 'German Democratic Republic':
            row[-1] = 'Germany'
        
        if row[-1].isdigit():
            del row[-1]
        
        Places.iloc[ind]['Born in'] = row
    
# Start creating the pie chart
Get_Nat(Places)

