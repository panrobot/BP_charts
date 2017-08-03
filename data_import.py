import array
import re
import math
import pandas as pd
from bs4 import BeautifulSoup



if __name__ == '__main__':
    
    def updateColumns(columns, page, position, value):
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
    nextCol = False
    probVal = False
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
                                pos = eval(textline['bbox'])
                                colsOnPages = updateColumns(colsOnPages, int(page['id']), math.floor(pos[2]), val)
                                val=''
                                probVal = False
                            #if it is not flush val and go to the next textline    
                            else:
                                val = ''
                            break
    for key in colsOnPages.keys():
        for k in colsOnPages[key].keys():
            print('Strona {0}, pozycja {1}, rowek: {2}'.format(key, k, colsOnPages[key][k]))
