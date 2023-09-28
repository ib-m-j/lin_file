import cards
import random
import bri
import os.path
import argparse
import glob
import datetime
import sys

def getCard(briValue):
    return  cards.allCards[briValue]

class LinTag:
    
    def __init__(self, tag, value = ''):
        self.tag = tag
        self.value = value

    def string(self):
        return '{}|{}|'.format(self.tag, self.value)

    

class LinDeal:
    multiLinFileTag = 'qx'
    setVulTag = 'sv'
    makeDealTag = 'md'
    pageBreakTag = 'pg'
    unknownTag = 'rh'
    boardTextTag = 'ah'

    def __init__(self, deal):
        self.tagList = [LinTag(LinDeal.multiLinFileTag, deal.makeBoardNo()),
                        LinTag(LinDeal.makeDealTag, deal.makeLinString()),
                        LinTag(LinDeal.unknownTag, ''),
                        LinTag(LinDeal.boardTextTag, 'Board {}'.format(deal.makeBoardText())),
                        LinTag(LinDeal.setVulTag, deal.getLinVul()),
                        LinTag(LinDeal.pageBreakTag)]
        
    def getTagLine(self):
        res = ''
        for (t) in self.tagList:
            res = res + t.string()
        return res


#inputFolder = os.path.join('.','input')
inputFolder = os.path.join('C:\\','BC3','kortfordelinger')
outputFolder = os.path.join('C:\\','bbokort')
#inputBaseName = '29-08-2023.bri'
#resultBaseName = inputBaseName.replace('bri', 'lin')
#inputFileName = os.path.join(inputFolder, inputBaseName)
#outputFileName = os.path.join(outputFolder, resultBaseName)

halfTableBreakBoard = 'qx|o{}|md|3SHDAKQJT98765432C,SHDCAKQJT98765432,SAKQJT98765432HDC,SHAKQJT98765432DC|rh||ah|Board {}|sv|0|pg||\n'
#halfTableInterval = 4
halTableStartBoard = 101


def makeLinFile(inputFileName, halfTableInterval, outputFileName):
    myBriFile = open(inputFileName,'rb')
    myLinFile = open(outputFileName,'w')

    allDeals = bri.getAllDeals(myBriFile)

    #print('halftable', halfTableBreakBoard)
    linText = ''
    dealNo = 0
    for d in allDeals:
        if (dealNo % halfTableInterval) == 0:
            breakNo = (dealNo // halfTableInterval) + 101
            linText = linText + halfTableBreakBoard.format(breakNo, breakNo)
            
        linData = LinDeal(d)
        linLine = linData.getTagLine()
        linText = linText + linLine + '\n'
        dealNo = dealNo + 1
    
    lastBreakNo = (dealNo // halfTableInterval) + 101

    linText = linText + halfTableBreakBoard.format(lastBreakNo, lastBreakNo)

    #print( linText)
    
    myLinFile.write(linText)
    myBriFile.close()
    myLinFile.close()

def getFilenameDate(fileName):
    datePart = os.path.splitext(os.path.split(fileName)[1])[0]
    components = datePart.split('-')
    return datetime.date(
        int(components[2]),int(components[1]),int(components[0]))
    print(datePart)


def getBestFile(possibleFiles):
    today = datetime.date.today()
    foundDate = None
    foundFile = None
    for f in possibleFiles:
        date = getFilenameDate(f)
        #print('testing date', date)
        if date <= today:
            if not(foundDate):
                foundDate = date
                foundFile = f
            else:
                if date > foundDate:
                    foundDate = date
                    foundFile = f

    if foundDate != today:
        print("\nWarning nit using todays file")

    return foundFile
            

def parseArguments():
    parser = argparse.ArgumentParser('make lin file')
    #parser.add_argument('input_deal_file', type=str)
    parser.add_argument('deals_per_round', type=int)
    parser.add_argument('-t', action='store_true')
    
    args = parser.parse_args()
    #print("args are ", args)

    return args.deals_per_round


def setFiles():
    possibleFiles = glob.glob(os.path.join(inputFolder,'*.bri'))
    #print(possibleFiles)
    input = getBestFile(possibleFiles)
    output = os.path.join(outputFolder, os.path.basename(input).replace('bri', 'lin'))
    return input, output


def runold():
    roundLength = sys.argv[1]
    possibleFiles = glob.glob(os.path.join(inputFolder,'*.bri'))
    #print(possibleFiles)
    res = getBestFile(possibleFiles)
    print('work with file:', res)
    print('set roun d length to:', roundLength) 

def run():
    rounds = parseArguments()
    input, output = setFiles()
    print('\nInputfile:', input)
    print('Óutputfile', output)
    print('Set half table interval to',rounds) 
    makeLinFile(input, rounds, output)


if __name__== '__main__':
    run()
