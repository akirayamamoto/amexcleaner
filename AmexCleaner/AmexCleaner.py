'''
Created on 13/01/2013

@author: Akira Yamamoto

Como utilizar:
    Instale a extensao Scraper do Chrome (https://chrome.google.com/webstore/detail/scraper/mbigbapnjcgaffohmbkdlecaccepngjd)
        ou algo similar;
    
    Exporte a tabela HTML da fatura SEM O CABECALHO para uma panilha do Google Drive;
    
    No Google Drive, clicar em File, Download as, CSV;
    
    Mova o arquivo para a mesma pasta deste script, salvando como input.csv;
    
    Execute este script, o arquivo de saida sera salvo como output.csv;

Input (no header):
    # Date, Description, Amount, Bill Start Date
    29/06/2012,Outflow description,R$ #.###,##, 01/06/2012
    30/06/2012,Inflow description,- R$ #.###,##, 01/06/2012

Output:
    Date,Payee,Category,Memo,Outflow,Inflow
    07/25/10,Sample Payee,,Sample Memo for an outflow,100.00,
    07/26/10,Sample Payee 2,,Sample memo for an inflow,,500.00
'''

import csv
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

def cleanString(stringToClean):
    # returns the string cleaned

    stringToClean = (stringToClean
        # removes non iso-8859-1 chars
        .decode('utf-8').encode('iso-8859-1', 'ignore')
        .decode('iso-8859-1').encode('utf-8')
        
        # similar to trim, will remove whitespaces from begin and end 
        .strip())
    
    return re.sub(r'[\s]+', ' ', stringToClean)  # replaces one or more whitespaces by only one

def cleanRow(row):
    # void, cleans the array in-place
    for (index, cell) in enumerate(row):
        row[index] = cleanString(cell)
    
def convertToYnabRow(row, inputDateFormat, outputDateFormat):
    # returns YNAB formatted row

    # from: Date, Description, Amount, Bill Start Date
    # to: Date, Payee, Category, Memo, Outflow, Inflow
    
    ynabRow = ['', '', '', '', '', '']
    
    transactionDate = datetime.strptime(row[0], inputDateFormat)
    ynabRow[0] = transactionDate.strftime(outputDateFormat)
    
    # row[1] description
    ynabRow[1] = row[1]
    
    # Memo
    installmentNum = re.search('COMPRA PARCELADA PRESTACAO (\d)+ DE', row[1], re.IGNORECASE)
    if installmentNum and int(installmentNum.group(1)) > 1: # prestacao > 1
        installmentDate = transactionDate
        
        billStartDate = datetime.strptime(row[3], inputDateFormat)
        
        while installmentDate < billStartDate: # data da prestacao < data inicial da fatura
            installmentDate += relativedelta(months=1) # data da prestacao += 1 mes 
        
        ynabRow[0] = installmentDate.strftime(outputDateFormat)
        ynabRow[3] = 'Data da compra: ' + transactionDate.strftime('%Y-%m-%d')
    else:
        ynabRow[3] = ''
    
    # row[2] from 'R$ #.###,##' to '####.##'
    row[2] = re.sub(r'[^(\d,\-)]+', '', row[2])  # removes anything but numbers, '-' and ','
    # row[2] = re.sub(r'[\sR$\.\-]+', '', row[2]) # removes whitespaces, 'R', '$', '-' and '.'
    row[2] = row[2].replace(',', '.')  # replaces the decimal separator from ',' to '.'
    
    moneyValue = float(row[2])  # positive number means debit in credit card bills
    if moneyValue > 0:
        ynabRow[4] = moneyValue  # outflow
    else:
        ynabRow[5] = -1 * moneyValue  # inflow
    
    return ynabRow

def processCsv(inputCsvFile, outputCsvFile, inputDelimiter, outputDelimiter, inputDateFormat, outputDateFormat):
    linesWritten = 0

    # read binary mode
    with open(inputCsvFile, 'rb') as readFile:
        
        # write binary mode
        with open(outputCsvFile, 'wb') as writeFile:
            
            reader = csv.reader(readFile, delimiter=inputDelimiter)
            writer = csv.writer(writeFile, delimiter=outputDelimiter)

            writer.writerow(['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow'])
            
            for row in reader:
                cleanRow(row)
                
                writer.writerow(convertToYnabRow(row, inputDateFormat, outputDateFormat))
                linesWritten += 1

    return linesWritten

def main():
    try:
        print str(processCsv('input.csv', 'output.csv',
                             inputDelimiter=',', outputDelimiter=',',
                             inputDateFormat='%d/%m/%Y', outputDateFormat='%d/%m/%Y'
                             )) + ' lines written'
    except Exception, exception:
        print 'Exception: ' + str(exception)
        pass

    input('Press enter to continue...')

if __name__ == '__main__':
    # when this script is called from command line we will call main()
    main()

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
