'''
Documentation, License etc.

@package bp_charts
'''
import re
import datetime as dt
import pandas as pd
import data_import

BoysHeight_0_5 = 'lhfa_boys_p_exp.txt'
BoysHeight_5_17 = 'hfa_boys_perc_WHO2007_exp.txt'
GirlsHeight_0_5 = 'lhfa_girls_p_exp.txt'
GirlsHeight_5_17 = 'hfa_girls_perc_WHO2007_exp.txt'

if __name__ == '__main__':
    
    def getHeightPercentile(height, dob, gender):
        percentiles = ['P01','P1','P3','P5','P10','P15','P25','P50','P75','P85','P90','P95','P97','P99','P999']
        age = dt.datetime.today() - dob
        genderTables = {'M' : {0 : BoysHeight_0_5, 1 : BoysHeight_5_17}, 'F' : {0: GirlsHeight_0_5, 1: GirlsHeight_5_17}}
        if age.days <= 1856:
            table = data_import.importCSV(genderTables[gender][0])
            row = table[(table.iloc[:,0] == age.days)]
        if 60 <= int(age.days / 30.4375) <= 228:
            table = data_import.importCSV(genderTables[gender][0])
            row = table[(table.iloc[:,0] == int(age.days / 30.4375))]
            
        pct = 'P01'
        for p in percentiles:
            if row[p].values[0] < height:
                pct = p
            else:
                break
        if pct in percentiles[0:4]:
            pct = 0
        elif pct in percentiles[4:6]:
            pct = 1
        elif pct == 'P25':
            pct = 2
        elif pct == 'P50':
            pct = 3
        elif pct == 'P75':
            pct = 4
        elif pct in percentiles[9:11]:
            pct = 5
        elif pct in percentiles[11:]:
            pct = 6
        return pct, p
                
        
    BPtable = pd.DataFrame()
    BPtable = data_import.importPDF(pdffile='child_tbl.pdf')
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
        if bpdia < 20 or bpdia > 120:
            bpdia = 0
            print('BP dia out of range')
        elif bpdia == '':
            print('No BP dia specified - app looking for a norm values')
            bpsys = ''
            break
    #gender = 'M'
    #height = 130
    #bpsys = 95
    #dob = dt.datetime(2015,8,8)
    pct, p = getHeightPercentile(height, dob, gender)
    age = dt.datetime.today() - dob
    age = int(age.days / 30.4375 / 12)
    if bpsys:
        result = BPtable[(BPtable['Age'] == age) & (BPtable.iloc[:,pct] <= bpsys) & (BPtable['Gender'] == gender)].loc[:,'BP_percentile']
        print('For gender {0} {1} year(s) old {2} cm high (it\'s within {3} percentile) with blood pressure systolic {4} mmHg - it is within {5}th percentile and for diastolic {6} mmHg it is within {7}th percentile of blood pressure norm'.
          format(gender, age, height, p, bpsys, BPtable[(BPtable['Age'] == age) & (BPtable['Gender'] == gender) & (BPtable.iloc[:,pct] >= bpsys)].loc[:,'BP_percentile'].values[0], bpdia,
                 BPtable[(BPtable['Age'] == age) & (BPtable['Gender'] == gender) & (BPtable.iloc[:,pct+7] >= bpdia)].loc[:,'BP_percentile'].values[0]))
    else:
        result = BPtable[(BPtable['Age'] == age) & (BPtable['BP_percentile'] == 90) & (BPtable['Gender'] == gender)]
        print('For gender {0} {1} year(s) old {2} cm high (it\'s within {3} percentile) proper blood pressure is: systolic {4} mmHg, diastolic {5} mmHg'.
          format(gender, age, height, p, BPtable[(BPtable['Age'] == age) & (BPtable['BP_percentile'] == 90) & (BPtable['Gender'] == gender)].iloc[:,pct].values[0],
                 BPtable[(BPtable['Age'] == age) & (BPtable['BP_percentile'] == 90) & (BPtable['Gender'] == gender)].iloc[:,pct+7].values[0]))
    
    
