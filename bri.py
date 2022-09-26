import cards

def briPos(x):
    return 'NES'.find(x)

def getHand(file, state):
    offSet = getOffset(state) 
    file.seek(offSet)
    allCards = file.read(26)
    res = []
    for x in range(0, 26, 2):
        res.append( cards.allCards[int(allCards[x : x+2])-1])
    return cards.Hand(res)


    def close(self):
        self.handle.close()

def getOffset(state):
    return (0x80* state[0]) + 26*briPos(state[1])

def advanceState(state):
    if state[1] == 'S':
        newDealNo = state[0] + 1
        newHand =  'N'
    elif state[1] == 'E':
        newDealNo = state[0]
        newHand = 'S'
    else:
        newDealNo = state[0]
        newHand = 'E'
    
    return (newDealNo, newHand)

def getAllDeals(file):
    curState = (0, 'N')
    offset = getOffset(curState)
    allDeals = []
    while True:
        if curState[1] == 'N':
            curDeal = cards.Deal(curState[0])
        try:
            newHand = getHand(file, curState)
        except:
            break
        curDeal.addHand(curState[1], newHand)
        if curState[1] == 'S':
            curDeal.checkOkHands()
            allDeals.append(curDeal)
        curState = advanceState(curState)
    
    return(allDeals)

def getCard(briValue):
    return  cards.allCards[briValue]


if __name__ == '__main__':
    myFile = open('07-06-2022.bri','rb')
    allDeals = getAllDeals(myFile)
    for d in allDeals:
        print(d)
    myFile.close()







#    myDeal = cards.Deal(2)
#    for seat in 'NES':
#        myDeal.addHand(seat, getHand(myFile, myDeal.dealNo, seat)) 
#    myDeal.checkOkHands()
#    print(myDeal)
##    print(myFile.getHand(0))
##    print(myFile.getHand(1))
#
#    myFile.close()
#
