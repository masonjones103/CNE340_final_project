import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


# urls for data
urls =  {"stats_drivers": "https://docs.google.com/spreadsheets/d/1QZ3EeNsdmd1R6Ahow5xr6Z_CcnvdHYm2uVXsivKFOa8/export?format=csv&gid=0"}

# creates engine for sql alchemy and mysql stuff
engine = create_engine('mysql+mysqlconnector://root:@localhost/mario_kart')

# loops each sheet and reads it into dataframe
for sheet_name, url in urls.items():
        print(f"Importing {sheet_name}...")

# reads csv data from url
        df = pd.read_csv(url, header=1)

# merging Driver and Unnamed: 2 columns
        if "Driver" in df.columns and "Unnamed: 2" in df.columns:
                df["Driver"] = df["Driver"].fillna(df["Unnamed: 2"])
                df.drop(columns=["Unnamed: 2"], inplace=True)

# Dropping last row/column
        df = df.drop(52, axis=0)

# saves dataframe to mysql
        df.to_sql(name=sheet_name, con=engine, if_exists="replace", index=False, method="multi")

print("data has been imported")
# ---------------------------------------------Kaylie's Coding----------------------------------------------------------
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

