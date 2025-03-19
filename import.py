# Kaylie Velazquez
# Mason Jones
# Will Dunlap
# 02/28/2025
# CNE 335
# Code performs data analytics on a database stored in WAMP using pandas code functions. In our code we are retrieving
# data from a Mario Kart google document and analyzing the data and executing it to a visual graph.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # install panda
from sqlalchemy import create_engine  # install sqlalchemy

# url for data
url = "https://docs.google.com/spreadsheets/d/1QZ3EeNsdmd1R6Ahow5xr6Z_CcnvdHYm2uVXsivKFOa8/export?format=csv&gid=0"

# creates engine using sql alchemy and mysql
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(user="root", pw="", host="127.0.0.1", db="mario_kart"))

print("Importing Drivers...")

# reads csv data from url
df = pd.read_csv(url, header=1)

# adds values to a column and drops unneeded column
if "Driver" in df.columns and "Unnamed: 2" in df.columns:
    df["Driver"] = df["Driver"].fillna(df["Unnamed: 2"])
    df.drop(columns=["Unnamed: 2"], inplace=True)

# drops unneeded last row
df = df.drop(52, axis=0)

# converts pandas dataframe to sql
df.to_sql(name='stats_drivers', con=engine, if_exists="replace", index=False, method="multi")

print("data has been imported")

# -----------------------------------------------Mason's Coding---------------------------------------------------------

input('''
Mason's new analysis:
Press enter:
''')

# column names stored as a list
column_names_list = ['WG', 'AC', 'ON', 'OF', 'MT', 'SL', 'SW', 'SA', 'SG', 'TL', 'TW', 'TA', 'TG', 'IV']

# takes the drivers names you would like to compare
def select_driver_one():
    driver_one = input('''Type the name of the first driver you would like to select.
    >''').title()
    return driver_one
def select_driver_two():
    driver_two = input('''Type the name of the second driver you would like to select.
    >''').title()
    return driver_two

# takes the name given from select_driver_#, iterates through each row of temp_table['Driver],
# dropping all text after '\n' if it appears, then if the given name is equal to the row's name,
# returns the row index and row's name
def find_driver(name):
    for row_i in range(len(df['Driver'])):
        og_name = df['Driver'].iloc[row_i]
        if '\n' in og_name:
            char_index = og_name.index('\n')
            og_name = og_name[:char_index]
        if name in og_name:
            return row_i, og_name

# takes the index of the driver and adds all but the first value, the name, to a list and returns that list
def remove_name(index):
    i = 0
    value_list = []
    for value in df.iloc[index]:
        if i >= 2:
            value_list.append(value)
        i += 1
    return value_list

# attempts to get the values of a driver you input, if the name is invalid a TypeError occurs and the function runs again.
def get_driver_one_values():
    try:
        driver_one_index, driver_one_name = find_driver(select_driver_one())
        driver_one_values = remove_name(driver_one_index)
        return driver_one_name, driver_one_values
    except TypeError:
        print('Driver not found, try again.')
        return get_driver_one_values()
def get_driver_two_values():
    try:
        driver_two_index, driver_two_name = find_driver(select_driver_two())
        driver_two_values = remove_name(driver_two_index)
        return driver_two_name, driver_two_values
    except TypeError:
        print('Driver not found, try again.')
        return get_driver_two_values()

# removes the star symbol from values and converts them to an integer
def remove_stars(values):
    i = 0
    for value in values:
        values[i] = value.replace('🟊', '')
        values[i] = int(values[i])
        i += 1
    return values

# compares driver values to find the one with the higher values and outputs the names and who is faster.
def compare_drivers(d1_name_input, d1_values_input, d2_name_input, d2_values_input):
    d1_combined_stats = d1_values_input[0] + d1_values_input[1] + d1_values_input[5]
    d2_combined_stats = d2_values_input[0] + d2_values_input[1] + d2_values_input[5]
    if d1_combined_stats > d2_combined_stats:
        return '\n> ' + d1_name_input + ' is faster than ' + d2_name_input + ' <'
    elif d1_combined_stats < d2_combined_stats:
        return '\n> ' + d2_name_input + ' is faster than ' + d1_name_input + ' <'
    else:
        return '\n> Drivers have equal speeds <'

# gets the drivers names and values of their stats
d1_name, d1_values = get_driver_one_values()
d2_name, d2_values = get_driver_two_values()

# removes the star symbol from the drivers values
d1_values_stars_removed = remove_stars(d1_values)
d2_values_stars_removed = remove_stars(d2_values)

# compares drivers values and prints the results
print(compare_drivers(d1_name, d1_values_stars_removed, d2_name, d2_values_stars_removed))
input('\nPress enter to see a graph comparing both drivers.')
print('''
WG = Weight, AC = Acceleration, ON = On-Road Traction, OF = Off-Road Traction, MT = Mini-Turbo, 
SL = Ground Speed, SW = Water Speed, SA = Anti-Gravity Speed, SG = Air Speed, 
TL = Ground Handling, TW = Water Handling, TA = Anti-Gravity Handling, TG = Air Handling, IV = Invincibility''')

# sets the plot size
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim(0, 10)

# plots both drivers data in a graph with the names stored in the legend
plt.plot(column_names_list, d1_values_stars_removed, label=d1_name)
plt.plot(column_names_list, d2_values_stars_removed, label=d2_name)
leg = plt.legend(loc='upper center')
plt.show()

# # ---------------------------------------------Kaylie's Coding----------------------------------------------------------
input('''
Kaylie's analysis:
Press enter:
''')
# Drivers vs. AC & WG
df = df.loc[:10]

if "AC" in df.columns and "OF" in df.columns:
    df["AC"] = pd.to_numeric(df["AC"], errors='coerce')
    df["OF"] = pd.to_numeric(df["OF"], errors='coerce')

    AC_M = df["AC"].mean()
    OF_M = df["OF"].mean()

    for drivers, row in df.iterrows():
        ac_dis_adv = "AC Advantage" if row["AC"] > AC_M else "AC Disadvantage"
        of_dis_adv = "OF Advantage" if row["OF"] > OF_M else "OF Disadvantage"
        print(f"{row['Driver']} has {ac_dis_adv} & {of_dis_adv}")

    bar_width = 0.40
    x = np.arange(len(df))
    plt.figure(figsize=(15, 6))
    plt.bar(x - bar_width / 2, df["AC"], label="AC", alpha=0.8, color='pink', width=bar_width)
    plt.bar(x + bar_width / 2, df["OF"], label="OF", alpha=0.8, color="purple", width=bar_width)

    plt.title("Driver vs AC & OF")
    plt.xlabel("Driver")
    plt.ylabel("AC & OF Stats")
    plt.xticks(x, df["Driver"], rotation=45)
    plt.grid(True)
    plt.legend()
    plt.show()  # Display bar graph
    plt.clf()  # Clears figure
    plt.close()  # Closes figure

# --------------------------------------------Will's Coding-----------------------------------------------------------
def remove_stars(values):
    return values.str.replace('🟊', '', regex=False).astype(float)

input(''' 
Will's analysis: 
Press enter: 
''')

# Load data
query = "SELECT * FROM stats_drivers"
df = pd.read_sql(query, con=engine)

# apply star function
df['WG'] = remove_stars(df['WG'])
df['AC'] = remove_stars(df['AC'])

# converts to numeric
df['WG'] = pd.to_numeric(df['WG'], errors='coerce')
df['AC'] = pd.to_numeric(df['AC'], errors='coerce')

#lists the top 3 and bottom 3 weights
lowest_wg = df.sort_values(by=['WG'], ascending=True).head(3)
highest_wg = df.sort_values(by=['WG'], ascending=False).head(3)

#prints names
print("\nCharacters with Lowest WG:")
print(lowest_wg[['Driver', 'WG']])

print("\nCharacters with Highest WG:")
print(highest_wg[['Driver', 'WG']])

speed_vs_weight = df.groupby('WG')['AC'].mean()

#plots graph
plt.figure(figsize=(10, 5))
plt.scatter(speed_vs_weight.index, speed_vs_weight.values, marker='o', linestyle='-', color='b')
for weight in range(1, 11, 2):
    plt.xticks(range(0, 11, 1))
plt.xlabel('Weight (WG)', fontsize=12)
plt.ylabel('Average Acceleration (AC)', fontsize=12)
plt.title('Weight vs. Acceleration in Mario Kart', fontsize=14, fontweight='bold')
plt.grid(True)
plt.show()
plt.clf()
plt.close()
