import pygsheets
path="C:\\Users\\Hp\\OneDrive\\Desktop\\internship\\scanner.json"
gc = pygsheets.authorize(service_account_file=path)
sheetname='cnk'
sh=gc.open(sheetname)
wks = sh.worksheet_by_title('std')

wks.update_value('A1',42)
wks.update_value('A2',45)

print('done')