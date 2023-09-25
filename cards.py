import random


class Suit:
    def __init__(self,x):
        self.suitId = x

    def __str__(self):
        return(self.suitId)

    def val(self):
        return 'SHDC'.find(self.suitId)

    def __lt__(self, other):
        if self.val() < other.val():
            return True
        
        return False
        
allSuits = [Suit('S'), Suit('H'), Suit('D'), Suit('C')]


class Value:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if  self.value == 1: 
            return 'A'
        elif self.value == 10:
            return 'T'
        elif self.value == 11:
            return 'J'
        elif self.value == 12:
            return 'Q'
        elif self.value == 13:
            return 'K'
        else:
            return str(self.value)

    def __gt__(self, other):
        if self.value == 1:
            return False
        else:
            return self.value < other.value

allValues = [Value(x) for x in range(1,14)]


class Card:
    def __init__(self, s,v):
        self.suit = s
        self.value = v
        
    def __str__(self):
        return self.suit.__str__()+self.value.__str__()+' '

    def __lt__(self, other):
        return self.suit < other.suit or (
            self.suit == other.suit and self.value < other.value)

    def getValue(self):
        return self.value.__str__()
        
    def getSuit(self):
        return self.suit.__str__()
        
               
#class Hand:
#    def __init__(self, cards):
#        self.cards = cards
#
#    def sortHand(self):
#        pass
#
class Hand:
    def __init__(self, listOfCards):
        self.cards = listOfCards
        self.cards.sort()
    
    def __str__(self):
        oldSuit = ''
        res = ''
        for c in self.cards:
            if c.suit != oldSuit:
                res = res+'\n{} {}'.format(c.suit, c.value)
                oldSuit = c.suit
            else:
                res = res + c.value.__str__()

        return res
        
    def __len__(self):
        return len(self.cards)

allSeats = ['N', 'E', 'W', 'S']
    
class Deal:
    def __init__(self, dealNo):
        self.dealNo = dealNo
        
        self.allHands = {x:Hand([]) for x in allSeats}

    def addHand(self, seat, hand):
        self.allHands[seat] = hand


    def __str__(self):
        res = 'Deal number {}\n'.format(self.dealNo)
        for k,v in self.allHands.items():
            res = res + '\nKey: {}'.format(k)
            res = res + v.__str__() + '\n'
        return res
        
    def checkOkHands(self):
        errorSeats = []
        usedCards = []
        for k,v in self.allHands.items():
            if len(v) != 13:
                errorSeats.append(k)
            usedCards = usedCards + v.cards
        if (len(errorSeats) == 1) and (len(usedCards) == 39):
            remainingCards = set(allCards).difference(set(usedCards))
            self.addHand(
                errorSeats[0], Hand(list(remainingCards)))
        #print('Adding {} cards to seat {}'.format(52 - 39, errorSeats[0]))


    def makeLinString(self):
        res = '{}'.format(self.getLinDealer())
        for k in 'SWNE':
            suit = ''
            for c in self.allHands[k].cards:
                if c.getSuit() != suit:
                    suit = c.getSuit()
                    res = res + c.getSuit()
                res = res + c.getValue() 
            res = res + ','
        return res[:-1]
                
            
        pass

    def makeBoardNo(self):
        return 'o{}'.format(self.dealNo + 1)

    def makeBoardText(self):
        return '{}'.format(self.dealNo + 1)

    def getLinVul(self):
        return '0neb'[((self.dealNo % 4) + (self.dealNo // 4)) % 4] 

    def getStdDealer(self):
        return 'NESV'[self.dealNo % 4] 

    def getLinDealer(self):
        return 'SVNE'.find(self.getStdDealer()) + 1

allCards = []
for suit in allSuits:
    for value in allValues:
        allCards.append(Card(suit,value))
allCards.sort()
#for c in allCards:
#    print (c, end = '')
#
#randomCards = random.sample(allCards, 13)
#randomHand = Hand(randomCards)
#print(randomHand)

