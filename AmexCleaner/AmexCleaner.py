'''
Created on 13/01/2013

@author: Akira

Tratar datas de compras parceladas, as datas sao do dia da compra, nao do dia da parcela
'''

import csv
import datetime
import re

def cleanString(stringToClean):
    # returns the string cleaned

    stringToClean = (stringToClean
        # removes non iso-8859-1 chars
        .decode('utf-8').encode('iso-8859-1', 'ignore')
        
        # similar to trim, will remove whitespaces from begin and end 
        .strip())
    
    return re.sub(r'[\s]+', ' ', stringToClean)  # replaces one or more whitespaces by only one

def cleanRow(row):
    # void, cleans the array in-place
    for (index, cell) in enumerate(row):
        row[index] = cleanString(cell)
    
def converToYnabRow(row):
    # returns YNAB row
    
    '''
    Date,Payee,Category,Memo,Outflow,Inflow
    07/25/10,Sample Payee,,Sample Memo for an outflow,100.00,
    07/26/10,Sample Payee 2,,Sample memo for an inflow,,500.00
    '''
    
    ynabRow = ['', '', '', '', '', '']
    
    # row[0] from '30/06/2012' to '06/30/2012'
    # try:
    ynabRow[0] = datetime.datetime.strptime(row[0], '%d/%m/%Y').strftime('%m/%d/%Y')
    # except ValueError, error:
    #    print str(error)
    #    pass
    
    # row[1] description
    ynabRow[1] = row[1]
    
    # Category
    ynabRow[2] = ''
    
    # Memo
    ynabRow[3] = ''
    
    # row[2] from 'R$ #.###,##' to '####.##'
    row[2] = re.sub(r'[^(\d,\-)]+', '', row[2])  # removes anything but numbers, '-' and '.'
    # row[2] = re.sub(r'[\sR$\.\-]+', '', row[2]) # removes whitespaces, 'R', '$', '-' and '.'
    row[2] = row[2].replace(',', '.')  # replaces the decimal separator from ',' to '.'
    
    moneyValue = float(row[2]) # generally positive number means debit
    if moneyValue > 0:
        ynabRow[4] = moneyValue # outflow
    else:
        ynabRow[5] = -1 * moneyValue # inflow
    
    return ynabRow

def main():
    inputDelimiter = ','
    outputDelimiter = ','
    
    inputCsvFile = 'input.csv'
    outputCsvFile = 'output.csv'
    
    with open(inputCsvFile, 'rb'  # read binary mode
              ) as readFile:
        with open(outputCsvFile, 'wb'  # write binary mode
                  ) as writeFile:
            
            reader = csv.reader(readFile, delimiter=inputDelimiter)
            writer = csv.writer(writeFile, delimiter=outputDelimiter)

            linesWritten = 0
            
            writer.writerow(['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow'])

            for row in reader:
                cleanRow(row)
                
                writer.writerow(converToYnabRow(row))
                linesWritten += 1

    print str(linesWritten) + ' lines written'

if __name__ == '__main__':
    try:
        # when this script is called from command line we will call main()
        main()
    except Exception, exception:
        print str(exception)
        pass

    input('Press enter to continue...')

'''
Date,Payee,Category,Memo,Outflow,Inflow
07/25/10,Sample Payee,,Sample Memo for an outflow,100.00,
07/26/10,Sample Payee 2,,Sample memo for an inflow,,500.00

INSTRUCTIONS: 1) Make your transactions look like the sample transactions above. (Those are just examples that you can delete) ,,,,,
(Every field can be left blank except the date. Valid date formats:
  DD/MM/YY
  DD/MM/YYYY
  DD/MM//YYYY
  MM/DD/YY
  MM/DD/YYYY
  MM/DD//YYYY
2) (Don't forget to delete all of these instructions from the file before you try to import it).,,,,,
3) Save this file.,,,,,
4) Shut down the program you're using to edit this file.,,,,,
5) Import this file into YNAB 3.,,,,,

http://scribu.net/blog/python-equivalents-to-phps-foreach.html

Looping over a list (Python)
items = ['orange', 'pear', 'banana']

# without indexes
for item in items:
    print item

# with indexes
for (i, item) in enumerate(items):
    print i, item

Looping over a dictionary (Python)
continents = {
    'africa': 'Africa',
    'europe': 'Europe',
    'north-america': 'North America'
}

# without keys
for continent in continents.values():
    print continent

# with keys
for (slug, title) in continents.items():
    print slug, title
'''
