class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.folded = False

    def reset_for_new_hand(self):
        self.hand = []
        self.current_bet = 0
        self.folded = False

    def __repr__(self):
        return f"{self.name} | Chips: {self.chips} | Hand: {self.hand}"

if __name__ == "__main__":
    from deck import Deck

    deck = Deck()
    p1 = Player("You")
    p2 = Player("Bot")

    p1.hand = deck.deal(2)
    p2.hand = deck.deal(2)

    print(p1)
    print(p2)
