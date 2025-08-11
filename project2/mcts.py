import math
import random
from dealer import Dealer
from deck import Deck


class Node:
    def __init__(self):
        self.N = 0
        self.W = 0.0
        self.children = {} 
    
    # Average reward
    def Q(self):
        return self.W / self.N if self.N else 0.0

def UCB1(current: Node, root_N: int, c: float = math.sqrt(2)) -> float:
    if current.N == 0:
        return float("inf")
    # V + c(sqrt(ln(N) / n))
    return current.Q() + c * math.sqrt(math.log(1, root_N) / current.N)

def remove_cards(deck, hand):
    return [card for card in deck if card not in hand]

class MCTS():
    def __init__(self, hand, 
                 epochs=1000, seed=42,
                 c=math.sqrt(2), cap_opp=1000,
                 cap_board=2000):

        if len(hand) != 2:
            print("Error... idk, placeholder or something")
        self.hand = hand
        self.epochs = epochs
        self.seed = random.Random(seed)
        self.c = c
        self.cap_opp = cap_opp
        self.cap_board = cap_board
        self.root = Node()
    
    # Avoid duplicates
    def _key(self, cards):
        print(cards)
        return tuple(sorted(cards))
    
    # Simulate an opponent hand
    def _new_opp(self, node: Node, deck: list):
        self.seed.shuffle(deck)
        opp_hand = [deck[-1], deck[-2]] # Grab the last 2 cards
        key = self._key(opp_hand)
        while key in node.children:
            self.seed.shuffle(deck)
            opp_hand = [deck[-1], deck[-2]]
            key = self._key(opp_hand)
        node.children[key] = Node()
        deck = [card for card in deck if card not in key]
        return (key, list(key), deck, node.children[key])

    # Simulate community
    def _new_board(self, node: Node, deck: list):
        self.seed.shuffle(deck)
        board = deck[-5:]
        key = self._key(board)
        while key in node.children:
            self.seed.shuffle(deck)
            board = deck[-5:]
            key = self._key(board)
        node.children[key] = Node()
        deck = [card for card in deck if card not in key]
        return (key, list(key), deck, node.children[key])
    
    def _ucb_child(self, node: Node):
        best_k = None
        best_ch = None
        best = float('-inf')
        for k, ch in node.children.items():
            value = UCB1(ch, node.N, self.c)
            if value > best:
                best_k = k
                best_ch = ch
                best = value
        return best_k, best_ch
    
    def estimate(self):
        wins= 0
        losses = 0
        ties = 0

        d = Deck()
        base_deck = d.create_deck()
        base_deck = remove_cards(base_deck, self.hand)

        for _ in range(self.epochs):
            path = [self.root]

            # Level 1 Opp
            opp_node  = self.root
            if len(opp_node.children) < self.cap_opp:
                key_opp, opp, opp_deck, opp_node = self._new_opp(opp_node, base_deck[:])
            else:
                key_opp, opp_node = self._ucb_child(opp_node)
                opp = list(key_opp)
                opp_deck = [card for card in base_deck if card not in key_opp]
            path.append(opp_node)

            # Level 2 Board
            board_node = opp_node
            if len(board_node.children) < self.cap_board:
                key_board, board, _, board_node = self._new_board(board_node, opp_deck)
            else:
                key_board, board_node = self._ucb_child(board_node)
                board = list(key_board)
            path.append(board_node)

            d = Dealer(base_deck)
            print("Len of Deck: ", len(base_deck))
            attend = (self.hand, opp)
            (winner, _) = d.calls(board, attend)
            if winner == "Player":
                wins += 1
                r = 1.0
            elif winner == "Environment":
                losses += 1
                r = 0.0
            else:
                ties += 1
                r = 0.5
            
            # Back prop
            for n in path:
                n.N += 1
                n.W += r
        total = wins + losses + ties
        equity = (wins + 0.5 * ties) / total if total else 0.0
        return (equity, {"wins": wins, "ties": ties, "losses": losses})

