from enum import Enum
from functools import reduce
import random
import socket
import sys
from struct import *

class Card:
    class SuitTypes(Enum):
        CLUBS = 0
        DIAMONDS = 1
        HEARTS = 2
        SPADES = 3

    def __init__(self, cardNum) -> None:
        if(cardNum > 51):
            raise ValueError("Given card number can not be greater than 51")
        elif(cardNum < 0):
            raise ValueError("Given card number can not be less than 0")
        self.cardNum = cardNum
        if(cardNum >= 0 and cardNum <= 12):
            self.suit = self.SuitTypes(0)
        elif(cardNum >= 13 and cardNum <= 25):
            self.suit = self.SuitTypes(1)
        elif(cardNum >= 26 and cardNum <= 38):
            self.suit = self.SuitTypes(2)    
        elif(cardNum >= 39 and cardNum <= 51):
            self.suit = self.SuitTypes(3)  
        self.rank = (cardNum % 13) + 2

    def __str__(self) -> str:
        return self.suit.name + ' of ' + str(self.rank)

    def __lt__(self, other) -> bool:
        if(not isinstance(other, Card)):
            return NotImplemented
        return self.rank < other.rank

    def __eq__(self, other) -> bool:
        if(not isinstance(other, Card)):
            return NotImplemented
        return self.rank == other.rank


class Deck:
    cards: list[Card]= [None]*52
    count = 0

    def __init__(self, *args) -> None:
        if(args):
            defaultCards = args[0]
            if(isinstance(defaultCards ,str)):
                self.cards = self.extractCardFromStrings(defaultCards)
            elif(isinstance(defaultCards, list)):
                for i in defaultCards:
                    if(i != None):
                        self.cards[i] = Card(i)
                self.count = len(defaultCards)
            else:
                raise(ValueError("Unsupported argument in deck __init__"))
        else:
            for i in range(0,52):
                self.cards[i] = Card(i)
            self.count = 52

    
    def extractCardFromStrings(self, cardList: str) -> list: 
        cards = [None]*52
        for i in range(0,len(cardList), 2):
            cardInt = int(cardList[i] + cardList[i+1])
            cards[cardInt] = Card(cardInt)
            self.count += 1
        return cards
    
    def addCard(self, card: Card) -> bool:
        if(self.cards[card.cardNum] == None):
            self.cards[card.cardNum] = card
            self.count += 1
            return True
        return False

    def removeCard(self, card : Card) -> bool:
        if(self.cards[card.cardNum] != None):
            self.cards[card.cardNum] = None
            self.count -= 1
            return True
        return False
        
    def deckString(self) -> str:
        strCard = []
        for card in self.cards:
            if(card != None):
                strCard.append(str(card))
        return strCard
    
    def giveCards(self) -> tuple:
        p1Deck = []
        p2Deck = []
        
        current = p1Deck
        while len(p1Deck) != 26 or len(p2Deck) != 26:
            if(len(current) == 26):
                current = p2Deck
            randomCard = random.randint(0, 51)
            if(self.cards[randomCard] != None):
                current.append(randomCard)
                self.cards[randomCard] = None
        self.count = 0
        return (p1Deck,p2Deck)


def main():
    args = sys.argv
    HOST = "127.0.0.1"
    PORT = 4444
    if(len(args) >= 2):
        HOST = args[1]
    if(len(args) >= 3):
        PORT = args[2]
    
    s = socket.socket()
    print(f"WAR server started on {HOST} {PORT}")
    print("Waiting for player...")

    s.bind((HOST, PORT))
    s.listen(2)
    
    c1,addr2 = s.accept()
    print("Player joined")
    
    c2,addr = s.accept()
    print("Player joined")
    
    deck = Deck()
    p1Msg = unpack("2B", c1.recv(2)) # wait for players want game command
    p2Msg = unpack("2B", c2.recv(2))
    if(p1Msg[0] != 0 or p2Msg[0] != 0):
        s.close()

    (p1Deck, p2Deck) = deck.giveCards()
    c1.sendall(pack('27B',1, *p1Deck))
    c2.sendall(pack('27B',1, *p2Deck))
    while(deck.count != 52):
        p1Msg = unpack("2B", c1.recv(2)) # wait for players cards
        p2Msg = unpack("2B", c2.recv(2)) 
        print("p1 message", p1Msg)
        print("p2 message", p2Msg)
        if(p1Msg[0] != 2 or p2Msg[0] != 2): # the only allowed command from  client at this stage is player card
            print("Client sent command other than 2.")
            s.close()                                       # if this is not the case then close socket probably buggy client
            break
        try:
            p1Card = Card(p1Msg[1]) #parse cards
            p2Card = Card(p2Msg[1])
        except ValueError:
            print("Buggy client, sent cards out of bound.")
            s.close()
            break
        deck.count += 2
        # see who won
        if(p1Card == p2Card): # its a tie
            c1.sendall(pack("2B", 3, 1))
            c2.sendall(pack("2B", 3, 1))
        elif(p1Card < p2Card): # player 1 wins
            c1.sendall(pack("2B", 3, 0))
            c2.sendall(pack("2B", 3, 2))
        else:  #player 2 wins
            c1.sendall(pack("2B", 3, 2))
            c2.sendall(pack("2B", 3, 0))
    print("Disconnecting....")
    s.close()

if __name__ == '__main__':
    main()