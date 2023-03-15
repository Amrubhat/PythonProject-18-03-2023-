import sqlite3
my_path="C:\\Users\\Hp\\OneDrive\\Desktop\\internship\\customer1.db" #Change the path 
my_conn = sqlite3.connect(my_path)
print("Connected to database successfully")


import pandas as pd
try:
    query="SELECT * FROM customer1" # query to collect record 
    df = pd.read_sql(query,my_conn,index_col='id') # create DataFrame
    print(df.head(4))
except sqlite3.Error as e:
    #print(e)
  error = str(e.__dict__['orig'])
  print(error)
else:
  print("DataFrame created successfully..") 

import pygsheets
path="C:\\Users\\Hp\\OneDrive\\Desktop\\internship\\scanner.json"
gc = pygsheets.authorize(service_account_file=path)
sheetname='cnk'
sh=gc.open(sheetname)
wks = sh.worksheet_by_title('std')

# wks.update_value('A1',42)
# wks.update_value('A2',45)

# print('done')
wks.clear()
wks.set_dataframe(df,(1,1),copy_index=True,extend=True)  
