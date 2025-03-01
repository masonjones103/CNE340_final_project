import pandas as pd
from sqlalchemy import create_engine

# urls for data
urls =  {
        "stats_drivers": "https://docs.google.com/spreadsheets/d/1QZ3EeNsdmd1R6Ahow5xr6Z_CcnvdHYm2uVXsivKFOa8/export?format=csv&gid=0",
        "stats_bodies": "https://docs.google.com/spreadsheets/d/1QZ3EeNsdmd1R6Ahow5xr6Z_CcnvdHYm2uVXsivKFOa8/export?format=csv&gid=1891506518",
        "stats_wheels": "https://docs.google.com/spreadsheets/d/1QZ3EeNsdmd1R6Ahow5xr6Z_CcnvdHYm2uVXsivKFOa8/export?format=csv&gid=54515627",
        "stats_gliders": "https://docs.google.com/spreadsheets/d/1QZ3EeNsdmd1R6Ahow5xr6Z_CcnvdHYm2uVXsivKFOa8/export?format=csv&gid=206723924",
}

# creates engine for sql alchemy and mysql stuff
engine = create_engine('mysql+mysqlconnector://root:@localhost/mario_kart')

# loops each sheet and reads it into dataframe
for sheet_name, url in urls.items():
        print(f"Importing {sheet_name}...")

# reads csv data from url
        df = pd.read_csv(url)

# saves dataframe to mysql
        df.to_sql(name=sheet_name, con=engine, if_exists="replace", index=False, method="multi")

print("data has been imported")
