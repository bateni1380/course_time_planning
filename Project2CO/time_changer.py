#requrements: 
#       windows operation system
#       install pywin32:   py -3.6 -m pip install pywin32
#       run with adminstrator access





import sys
import datetime

def present_time():

    from datetime import datetime, timedelta

    my_list = str(datetime.today() - timedelta(hours=3, minutes=30)).split(" ")
    date = my_list[0].split("-")
    day = date[-1]
    date[-1]= datetime.today().isoweekday()
    date.append(day)
    time = my_list[1].split(":")
    sec, mil = time[-1].split(".")
    time[-1] = int(sec)
    time.append(int(mil[0:2]))
    whole = date + time
    whole = tuple(map(int, whole))

    return whole
    

license_gams_25 = ( 2014, # Year
                  1, # Month
                  3, # Day of Week
                  1, # Day
                  0, # Hour
                  0, # Minute
                  0, # Second
                  0, # Millisecond
              )


present = present_time()

def win_back(license_gams = license_gams_25):
    import win32api
    win32api.SetSystemTime(*license_gams)


def win_update(time = present):
    import win32api
    win32api.SetSystemTime(*time)

print("changing time to use license...")
