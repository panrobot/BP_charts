import array
import re
import math
import pandas as pd
from bs4 import BeautifulSoup



if __name__ == '__main__':
    
    #colSys = [196,223,250,278,305,332,360]
    actCol = 0
    nextCol = False
    with open('out.xml', 'r', encoding='utf-8') as XMLinput:
        xml = BeautifulSoup(XMLinput, 'html.parser')
        pages = xml.find_all('page', id=re.compile('[1]'))
        val = ''
        for page in pages:
            textboxes = page.find_all('textbox', recursive=False)
            for textbox in textboxes:
                textlines = textbox.find_all('textline')
                for textline in textlines:
                    pos = eval(textline['bbox'])
                    for cs in colSys:
                        if math.floor(pos[2]) == cs:
                            nextCol = True
                            texts = textline.find_all('text')
                            for text in texts:
                                if re.match(r'\d', text.string):
                                    val += text.string
                                if re.match(r'\n', text.string):
                                    #print(val)
                                    val = ''
                if nextCol:
                    #print(textline['bbox'])
                    #print('To była kolumna {0}'.format(actCol))
                    actCol += 1
                    #print('Nastepna kolumna {0}'.format(actCol))
                    nextCol = False
                    
