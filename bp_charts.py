'''
Documentation, License etc.

@package bp_charts
'''
import re
import datetime as dt
import pandas as pd
import data_import

if __name__ == '__main__':
    
    BoysHeight_0_5 = pd.DataFrame()
    BoysHeight_5_17 = pd.DataFrame()
    GirlsHeight_0_5 = pd.DataFrame()
    GirlsHeight_5_17 = pd.DataFrame()
    with open('lhfa_boys_p_exp.txt', mode='r', encoding='utf-8') as boys_0_5:
        BoysHeight_0_5 = pd.read_csv(boys_0_5, sep = '\s+', header = 0, index_col = 0)
    with open('hfa_boys_perc_WHO2007_exp.txt', mode='r', encoding='utf-8') as boys_5_17:
        BoysHeight_5_17 = pd.read_csv(boys_5_17, sep = '\s+', header = 0, index_col = 0)
    with open('lhfa_girls_p_exp.txt', mode='r', encoding='utf-8') as girls_0_5:
        GirlsHeight_0_5 = pd.read_csv(girls_0_5, sep = '\s+', header = 0, index_col = 0)
    with open('hfa_girls_perc_WHO2007_exp.txt', mode='r', encoding='utf-8') as girls_5_17:
        GirlsHeight_5_17 = pd.read_csv(girls_5_17, sep = '\s+', header = 0, index_col = 0)
    dob = 0
    while dob == 0:
        dob = input('Enter date of birth as YYYY/MM/DD e.g 2000/12/01: ')
        try:
            dob = re.sub('[^0-9]', '', dob)
            dob = dt.datetime.strptime(dob, '%Y%m%d')
            if dt.datetime.today() - dob < dt.timedelta(days=0) or dt.datetime.today() - dob > dt.timedelta(days=42000):
                dob = 0
                print('Date out of range!')
        except:
            dob = 0
            print('Wrong date format')
    height = 0
    while height == 0:
        height = input('Enter height in cm: ')
        try:
            height = int(height)
        except:
            print('Wrong input!')
            height = 0
        if height < 44 or height > 200:
            height = 0
            print('Height out of range')
    gender = 0
    while gender == 0:
        gender = input('Enter gender as F or M: ')
        if gender not in ['f', 'F', 'm', 'M']:
            gender = 0
            print('Wrong gender')
        else:
            gender = gender.upper()
    bpsys = 0
    while bpsys == 0:
        bpsys = input('Enter Systolic Blood Pressure in mmHg (if empty, app will show norm): ')
        try:
            bpsys = int(bpsys)
        except:
            if bpsys != '':
                print('Wrong input!')
            else:
                print('No BP sys specified - app looking for a norm values')
                break
        if bpsys < 70 or bpsys > 180:
            bpsys = 0
            print('BP sys out of range')
        elif bpsys == '':
            print('No BP sys specified - app looking for a norm values')
            break
    bpdia = 0
    while bpdia == 0:
        if bpsys == '':
            print('No need for BP dia reading - app is looking for a norm values')
            break
        bpdia = input('Enter Systolic Blood Pressure in mmHg (if empty, app will show norm): ')
        try:
            bpdia = int(bpdia)
        except:
            if bpdia != '':
                print('Wrong input!')
            else:
                print('No BP dia specified - app looking for a norm values')
                break
        if bpdia < 70 or bpdia > 180:
            bpdia = 0
            print('BP dia out of range')
        elif bpdia == '':
            print('No BP dia specified - app looking for a norm values')
            bpsys = ''
            break
