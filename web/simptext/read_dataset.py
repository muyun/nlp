# -*- coding: utf-8 -*-
# coding by wenlong

import openpyxl

#read the dataset
filename = '/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/wordlist.xlsx'
wb = openpyxl.load_workbook(filename)
sheet = wb.get_sheet_by_name('level 1')

#store the simplied words in the simp_words list
simp_words=[]
for x in range(1, sheet.max_row+1):
    simp_words.append(str(sheet.cell(row=x,column=1).value))

# now removing it
#TODO- the replace function
