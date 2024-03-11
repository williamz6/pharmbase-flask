import datetime


# today_date = datetime.date.today()
# in_time = input("Enter date: ")
birthday = input("What is your birthday?")
birthday = datetime.datetime.strptime(birthday,"%d/%m/%Y").date()
print(birthday - datetime.date.today())
if birthday < datetime.date.today():
    print("your birthday has passed")
else:
    print("error")