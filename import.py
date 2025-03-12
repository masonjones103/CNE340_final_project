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
