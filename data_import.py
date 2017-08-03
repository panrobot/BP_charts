import re
import math
import pandas as pd
from bs4 import BeautifulSoup



if __name__ == '__main__':
    
    def updateColumns(columns, page, position, value):
        value = int(value)
        try:
            columns[page][position].append(value)
        except:
            if page not in columns.keys():
                columns[page] = {position : [value]}
            else:
                columns[page][position] = [value]
        return columns
            
        
    colsOnPages = {}
    actCol = 0
    probVal = False
    columns = ['Gender','Age','BP_percentile', 'BPSys_5Hp', 'BPSys_10Hp', 'BPSys_25Hp', 'BPSys_50Hp', 'BPSys_75Hp', 'BPSys_90Hp', 'BPSys_95Hp',
               'BPDia_5Hp', 'BPDia_10Hp', 'BPDia_25Hp', 'BPDia_50Hp', 'BPDia_75Hp', 'BPDia_90Hp', 'BPDia_95Hp'
               ]
    BPdb = pd.DataFrame()
    with open('out.xml', 'r', encoding='utf-8') as XMLinput:
        xml = BeautifulSoup(XMLinput, 'html.parser')
        pages = xml.find_all('page')
        val = ''
        for page in pages:
            textboxes = page.find_all('textbox', recursive=False)
            for textbox in textboxes:
                textlines = textbox.find_all('textline')
                for textline in textlines:
                    texts = textline.find_all('text')
                    for text in texts:
                        #check if we just found a digit in text segment
                        if re.match(r'\d', text.string):
                            val += text.string
                            #check if previously we have found digit and now our number is greater than 17 (BP can not be lower than 17 mmHg)
                            if len(val) > 1 and int(val) > 17:
                                probVal = True
                            #if we have found just one digit or number is lower than 17 it can not be a value we are looking for
                            else:
                                probVal = False
                        #check if we did not find a letter t from 'th' string or % symbol following our val
                        elif (text.string == 't' or text.string == r'%') and val != '':
                            val = ''
                            probVal = False
                            break
                        #check if we did find an empty string
                        elif re.match(r'\D', text.string):
                            #if it is an empty string and our val is probably a value let store it
                            if probVal == True:
                                pos = eval(text['bbox'])
                                colsOnPages = updateColumns(colsOnPages, int(page['id']), math.floor(pos[2]), val)
                                val=''
                                probVal = False
                            #if it is not flush val and go to the next textline    
                            else:
                                val = ''
    percentiles = [50, 90, 95, 99]
    for key in colsOnPages.keys():            
        positions = list(colsOnPages[key].keys())
        positions.sort()
        Pct = pd.DataFrame()
        Age = pd.DataFrame()
        BP = pd.DataFrame()
        if key % 2 == 0:
            age = [11]
        else:
            age = [1]
        ageBin = 0
        for idx, val in enumerate(positions):
            df = pd.DataFrame({columns[idx+3] : colsOnPages[key][positions[idx]]})
            BP = pd.concat([BP,df], axis=1)
        while ageBin < len(BP) / 4:
            df = pd.DataFrame({'Age' : age * 4})
            age[0] = age[0] + 1
            ageBin += 1
            Age = pd.concat([Age, df], axis=0)
            df = pd.DataFrame({'BP_percentile':percentiles})
            Pct = pd.concat([Pct, df], axis=0)
        Age = Age.reset_index(drop=True)
        Pct = Pct.reset_index(drop=True)
        if key == 1 or key == 2:
            gen = ['M']
            df = pd.DataFrame({'Gender' : gen * len(BP)})
            BP = pd.concat([BP,df], axis=1)
        else:
            gen = ['F']
            df = pd.DataFrame({'Gender' : gen * len(BP)})
            BP = pd.concat([BP,df], axis=1)
        BP = pd.concat([BP,Age], axis = 1)
        BP = pd.concat([BP,Pct], axis = 1)
        BPdb = pd.concat([BPdb, BP], axis = 0)
    BPdb = BPdb.reset_index(drop=True)
    BPdb.to_csv('BPdata.csv')
    #result = BPdb.loc[(BPdb['Age'] == 5) & (BPdb['Gender'] == 'M') & (BPdb['BPSys_5Hp'] < 110)]
    #print(result.loc[result.index.values[-1],'BP_percentile'])
    
    
            
            
