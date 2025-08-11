import calls


class Dealer():
    def __init__(self, deck):
        self.deck = deck
        self.rank_names = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8",
                           9: "9", 10: "10", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
        self.combo = {0: "Hight-Card", 1: "Pair of Ones", 2: "Two of Pairs",
                      3: "Three of a Kind", 4: "Straight", 5: "Flush", 6: "Full House",
                      7: "Four of a Kind", 8: "Straight Flush", 9: "Royal Flush"}
    
    def deal(self):
        return self.deck.pop()

    def speak(self, owner: str, hand: list) -> str:
        print("\n ")
        print(owner)
        for (rank, suit) in hand:
            print(f"{self.rank_names[rank]} of {suit}")
    
    def calls(self, community, attendees):
        player = attendees[0]
        environment = attendees[1]

        p_score = 0
        e_score = 0

        # Function Dispatch
        dispatch = [calls.royal_flush, calls.straight_flush, 
                    calls.four_kind, calls.full_house, calls.flush,
                    calls.straight, calls.three_kind, calls.two_pair,
                    calls.one_pair, calls.high_card]
        
        # Player
        for call in dispatch:
            p_score = call(community, player)
            if p_score > 0:
                break
        
        # Environment
        for call in dispatch:
            e_score = call(community, environment)
            if e_score > 0:
                break
            
        print(p_score, e_score)
        # Winner
        if p_score > e_score:
            print(self.combo[int(p_score)])
            return ("Player", p_score)
        elif p_score < e_score:
            print(self.combo[int(e_score)])
            return ("Environment", e_score)
        else:
            print("Tie")
            return ("Tie", -1)

