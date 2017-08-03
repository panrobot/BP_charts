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
        pages = xml.find_all('page', id=re.compile('[1]'))
        val = ''
        for page in pages:
            textboxes = page.find_all('textbox', recursive=False)
            for textbox in textboxes:
                textlines = textbox.find_all('textline')
                for textline in textlines:
                    texts = textline.find_all('text')
                    for text in texts:
                        if re.match(r'\d', text.string):
                            val += text.string
                            if len(val) > 1:
                                probVal = True
                            else:
                                probVal = False
                        elif text.string == 't' and val != '':
                            val = ''
                            probVal = False
                        elif re.match(r'\D', text.string):
                            if probVal == True:
                                pos = eval(textline['bbox'])
                                colsOnPages = updateColumns(colsOnPages, page['id'], math.floor(pos[2]), val)
                                val=''
                                probVal = False
                            break
