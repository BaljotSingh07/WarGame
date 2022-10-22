import unittest
from WarServer import Card, Deck, cardListToString

class TestCard(unittest.TestCase):
    def test_noargs(self):
        with self.assertRaises(TypeError):
            Card()

    def test_aces(self):
        card = Card(0)
        self.assertEqual("CLUBS of 2", str(card))

    def test_aces2(self):
        card = Card(13)
        self.assertEqual("DIAMONDS of 2", str(card))

    def test_lastcar(self):
        card = Card(51)
        self.assertEqual("SPADES of 14", str(card)) # 14 is ace

    def test_wrongcardnum(self):
        with self.assertRaises(ValueError):
            Card(52)
    
    def test_negcardnum(self):
        with self.assertRaises(ValueError):
            Card(-1)
    
    def test_equal(self):
        card = Card(0)
        card2 = Card(13)
        self.assertTrue(card == card2)
    
    def test_lessthan(self):
        card = Card(0)
        card2 = Card(14)
        self.assertFalse(card == card2)
        self.assertTrue(card < card2)

class TestDeck(unittest.TestCase):
    def test_str(self):
        correct = ["CLUBS of 2","CLUBS of 3","CLUBS of 4","CLUBS of 5","CLUBS of 6","CLUBS of 7",
                   "CLUBS of 8","CLUBS of 9", "CLUBS of 10", "CLUBS of 11", "CLUBS of 12", "CLUBS of 13", "CLUBS of 14",

                   "DIAMONDS of 2","DIAMONDS of 3","DIAMONDS of 4","DIAMONDS of 5","DIAMONDS of 6","DIAMONDS of 7",
                   "DIAMONDS of 8","DIAMONDS of 9", "DIAMONDS of 10", "DIAMONDS of 11", "DIAMONDS of 12", "DIAMONDS of 13", "DIAMONDS of 14",

                   "HEARTS of 2","HEARTS of 3","HEARTS of 4","HEARTS of 5","HEARTS of 6","HEARTS of 7",
                   "HEARTS of 8","HEARTS of 9", "HEARTS of 10", "HEARTS of 11", "HEARTS of 12", "HEARTS of 13", "HEARTS of 14",

                   "SPADES of 2","SPADES of 3","SPADES of 4","SPADES of 5","SPADES of 6","SPADES of 7",
                   "SPADES of 8","SPADES of 9", "SPADES of 10", "SPADES of 11", "SPADES of 12", "SPADES of 13", "SPADES of 14",
                    ]
        deck = Deck()
        self.assertListEqual(correct, deck.deckString())
    
    def test_removeCard(self):
        deck = Deck()
        removed = deck.removeCard(Card(50))
        self.assertTrue(removed)
        self.assertIsNone(deck.cards[50])
    
    def test_removeCard_twice(self):
        deck = Deck()
        removed = deck.removeCard(Card(0))
        self.assertTrue(removed)
        removed = deck.removeCard(Card(0))
        self.assertFalse(removed)
        
    def test_removeCard_invalidarg(self):
        deck = Deck()
        with self.assertRaises(ValueError):
            deck.removeCard(Card(-1))
        
    def test_givecards(self):
        (p1Deck, p2Deck) = Deck().giveCards()
        
        self.assertEqual(26, len(p1Deck), "player 1 deck does not contain 26 cards")
        self.assertEqual(26, len(p2Deck), "player 2 deck does not contain 26 cards")
        combined = p1Deck + p2Deck
        for i in range(0,52):
            self.assertEqual(1, combined.count(i), f"{i} count is not correct")
            
    def test_cardfromstr(self):
        correct = Deck([None,Card(1),Card(2),Card(3),Card(4),Card(5),Card(6),Card(7),Card(8),Card(9),Card(10)]+[None]*41)
        deck = Deck("01020304050607080910")
        self.assertListEqual(correct.deckString(), deck.deckString())
        self.assertEqual(deck.count, 10)
    
    def test_cardoflisttostring(self):
        deck = cardListToString([9,1,45])
        self.assertEqual("090145", deck)
        
if __name__ == '__main__':
    unittest.main()