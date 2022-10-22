import socket
import sys
import random
from WarServer import Card, Deck

def generateRadomCard(deck : Deck):
    card = None
    while card == None:
        ran = random.randint(0,51)
        if(deck.cards[ran] != None):
            card = Card(ran)
            deck.removeCard(card)
    return card         

def main():
    args = sys.argv
    HOST = "127.0.0.1"
    PORT = 4444
    if(len(args) >= 2):
        HOST = args[1]
    if(len(args) >= 3):
        PORT = args[2]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"0")
        data = s.recv(27*2 + 1).decode('utf-8')
        print("Recived cards from the server " + data + " with length " + str(len(data)))
        if(data[0] != "1"): # making sure server is working
            raise(TypeError("Server should have send game start command")) # throw meaningful error
        
        deck = Deck(data[1:]) # create deck from the server
        print("The deck after reciving cards from the server " + str(deck.deckString()))
        if(deck.count != 26):
            raise(ValueError("Server should have send 26 cards but only got ") + deck.count)
        #game repeats until the client has 0 cards
        while(deck.count != 0):
            card = generateRadomCard(deck)
            #set card to server
            print("You send " + str(card))
            s.sendall(b'2' + (str(card.cardNum).encode()))
            #get the server result
            servermsg = s.recv(4).decode('utf-8')
            print("server msg :" + servermsg)
            if(servermsg == ''):
                print("Server closed.")
                break
            if(servermsg[1:] == "0"): # you won
                print("You won")
            elif(servermsg[1] == "1"): # its a tie
                print("Its a tie")
            else: # you lost
                print("You lost")            
        print("Disconneting....")
        s.close()


if __name__ == '__main__':
    main()