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
inputFolder = os.path.join('C:\\','users','ibmjo','github','lin_file','input')
outputFolder = os.path.join('.','output')
inputBaseName = '29-08-2023.bri'
resultBaseName = inputBaseName.replace('bri', 'lin')
inputFileName = os.path.join(inputFolder, inputBaseName)
outputFileName = os.path.join(outputFolder, resultBaseName)
halfTableBreakBoard = 'qx|o{}|md|3SHDAKQJT98765432C,SHDCAKQJT98765432,SAKQJT98765432HDC,SHAKQJT98765432DC|rh||ah|Board {}|sv|0|pg||\n'
#halfTableInterval = 4
halTableStartBoard = 101


def makeLinFile(filename, halfTableInterval):
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
    
    print("Writing to ", outputFileName)
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
        print('testing date', date)
        if date <= today:
            if not(foundDate):
                foundDate = date
                foundFile = f
            else:
                if date > foundDate:
                    foundDate = date
                    foundFile = f
    return foundFile
            

def parseArguments():
    parser = argparse.ArgumentParser('make lin file')
    #parser.add_argument('input_deal_file', type=str)
    parser.add_argument('deals_per_round', type=int)
    args = parser.parse_args()
    print("args are ", args)
    
    possibleFiles = glob.glob(os.path.join(inputFolder,'*.bri'))
    print(possibleFiles)
    res = getBestFile(possibleFiles)
    print('\nWork with file:', res)
    print('Set half table interval to',args.deals_per_round) 
    return res, args.deals_per_round


def runold():
    roundLength = sys.argv[1]
    possibleFiles = glob.glob(os.path.join(inputFolder,'*.bri'))
    #print(possibleFiles)
    res = getBestFile(possibleFiles)
    print('work with file:', res)
    print('set roun d length to:', roundLength) 

def run():
    f, rounds = parseArguments()
    makeLinFile(f, rounds)


if __name__== '__main__':
    run()
