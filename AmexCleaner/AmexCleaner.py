# -*- coding: utf-8 -*-
'''
Created on 13/01/2013

@author: Akira
'''

import csv
import re

def main():
    with open('amex.csv', 'rb') as readFile:
        with open('output.csv', 'wb') as writeFile:
            reader = csv.reader(readFile, delimiter=',')
            writer = csv.writer(writeFile, delimiter=',')
            for row in reader:
                # data
                row[0] = row[0].encode('ascii', 'ignore').strip()
                row[0] = re.sub(r'[\s]+', ' ', row[0])
                
                # descricao
                row[1] = row[1].encode('ascii', 'ignore').strip()
                row[1] = re.sub(r'[\s]+', ' ', row[1])
                
                # valor em Reais
                row[2] = row[2].encode('ascii', 'ignore').strip()
                row[2] = re.sub(r'[\sR$\.]+', '', row[2])
                #row[2] = row[2].replace(',', '.') # formato americano
                
                writer.writerow(row)
                #print ', '.join(row)

if __name__ == '__main__':
    main()
