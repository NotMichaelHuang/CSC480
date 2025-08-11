from deck import Deck
from dealer import Dealer
from mcts import MCTS


def game():
    deck = Deck()
    cards = deck.create_deck()

    dealer = Dealer(cards)
    
    # Start Game
    player = []
    environment = []
    attendees = (player, environment)

    community = []
    burn_pile = [] # Debug purposes?
    toggle = True
    while toggle:
        # Deal cards 1 per rotation and 2 per player
        for _ in range(len(attendees)):
            # Feels like it could be more optimize
            for attendee in attendees:
                if len(attendee) < 2:
                    attendee.append(dealer.deal())

        mcts = MCTS(
            hand=player,
            epochs=5000,
            seed=42
            )
        equity, counts = mcts.estimate()
        print("\n")
        print("=" * 80)
        print("Env Hand", environment)
        print(f"Pre-flop Equity: {equity:.3f}  W/T/L: {counts}")
        print("=" * 80)
        print("\n")

        # Flop
        burn_pile.append(dealer.deal())
        for _ in range(3):
            community.append(dealer.deal())
        print("-Flop Phase")

        # Turn
        burn_pile.append(dealer.deal())
        community.append(dealer.deal())
        print("-Turn Phase")

        # River
        burn_pile.append(dealer.deal())
        community.append(dealer.deal())
        print("-River Phase")

        dealer.speak("Community", community)
        dealer.speak("Player", player)
        dealer.speak("Environment", environment)
        
        (winner, call) = dealer.calls(community, attendees)
        quit()


def main(): 
    while True:
        print("Play: 1")
        print("Quit: 2")
        user_input = int(input())
        if user_input == 1:
            game()
            # Run the game
        elif user_input == 2: 
            # Quit game
            quit()

if __name__ == "__main__":
    main()

