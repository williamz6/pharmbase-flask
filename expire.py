from datetime import datetime, date

expiry_date= '2023-10-24 00:00:00'
ExpirationDate = datetime.strptime(expiry_date,"%Y-%m-%d %H:%M:%S").date()
now= date.today()
print (now)
if ExpirationDate >= now:
    print('true')
else:
    print('false')