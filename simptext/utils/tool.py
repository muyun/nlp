# -*- coding: utf-8 -*-
"""
   utils.tool
   ~~~~~~~~~~
   common tool
"""

def read_file(filename):
   """ read the file and store the lines in a list
   """
   lines = []

   f = open(filename, 'rU')
   for line in f:
       lines.append(line)

   f.close()
