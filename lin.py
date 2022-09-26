import cards
import random
import bri
import os.path

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


inputFolder = os.path.join('.','input')
outputFolder = os.path.join('.','output')
inputBaseName = '07-06-2022.bri'
resultBaseName = inputBaseName.replace('bri', 'lin')
inputFileName = os.path.join(inputFolder, inputBaseName)
outputFileName = os.path.join(outputFolder, resultBaseName)
halfTableBreakBoard = 'qx|o{}|md|3SHDAKQJT98765432C,SHDCAKQJT98765432,SAKQJT98765432HDC,SHAKQJT98765432DC|rh||ah|Board {}|sv|0|pg||\n'
halfTableInterval = 4
halTableStartBoard = 101

if __name__== '__main__':
    myBriFile = open(inputFileName,'rb')
    myLinFile = open(outputFileName,'w')
    allDeals = bri.getAllDeals(myBriFile)

    print('halftable', halfTableBreakBoard)
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
    
    print("writing to ", outputFileName)
    lastBreakNo = (dealNo // halfTableInterval) + 101

    linText = linText + halfTableBreakBoard.format(lastBreakNo, lastBreakNo)

    print( linText)
    
    myLinFile.write(linText)
    myBriFile.close()
    myLinFile.close()

