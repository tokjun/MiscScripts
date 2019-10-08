#! /usr/bin/python

import sys, csv
import operator

inputFileName = None

sortKey = None
direction = None

for arg in sys.argv:
    param = arg.split('=', 2)
    if param[0] == 'IN':
        inputFileName = param[1]
    if param[0] == 'OUT':
        outputFileName = param[1]
    elif param[0] == 'KEY':
        sortKey = param[1]
    elif param[0] == 'DIR': # ascend or descend
        direction = param[1]

if inputFileName==None or outputFileName==None or sortKey==None:
    print('Usage: %s IN=<input CSV file> OUT=<outputCSV file> KEY=<key> DIR=<direction>' % (sys.argv[0]))
    print('      <input CSV file>  : Input CSV file.')
    print('      <output CSV file> : Output CSV file.')
    print('      <key>             : Key column for sorting')
    print('      <direction>       : Either "ascent" or "descent"')
    sys.exit()

if direction==None:
    direction = 'ascent'
 
with open(inputFileName) as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    lineCount = 0
    keys = csvReader.next()

    r = 0
    keyIndex = -1
    for key in keys:
        if key == sortKey:
            keyIndex = r
        r = r + 1
    
    if keyIndex < 0:
        print('There is no row named: %s' % (sortKey))
        sys.exit()

    print('key: %d' % (keyIndex))
    r = (direction == 'descent')
    sortedlist = sorted(csvReader, key=lambda x: float(x[keyIndex]), reverse=r)
    with open(outputFileName, "wb") as f:
        fileWriter = csv.writer(f, delimiter=',')
        fileWriter.writerow(keys)
        for row in sortedlist:
            fileWriter.writerow(row)



