import sqlite3
import pygsheets
my_path="C:\\Users\\Vinuta\\OneDrive\\Documents\\GitHub\\PythonProject-18-03-2023-\\attendance.db" #Change the path 
my_conn = sqlite3.connect(my_path)
print("Connected to database successfully")


import pandas as pd
try:
    query="SELECT * FROM attendance" # query to collect record 
    df = pd.read_sql(query,my_conn,index_col='id') # create DataFrame
    print(df.head(4))
except sqlite3.Error as e:
    #print(e)
  error = str(e.__dict__['orig'])
  print(error)
else:
  print("DataFrame created successfully..") 


path="C:\\Users\\Vinuta\\OneDrive\\Documents\\GitHub\\PythonProject-18-03-2023-\\scanner.json"
gc = pygsheets.authorize(service_account_file=path)
sheetname='cnk'
sh=gc.open(sheetname)
wks = sh.worksheet_by_title('std')

# wks.update_value('A1',42)
# wks.update_value('A2',45)

# print('done')
wks.clear()
wks.set_dataframe(df,(1,1),copy_index=True,extend=True)  
