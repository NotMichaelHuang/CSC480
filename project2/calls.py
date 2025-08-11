from collections import Counter


def _strip_suits(hand: list) -> list:
    return [suit for _, suit in hand]

def _strip_rank(hand: list) -> list:
    return [rank for rank, _ in hand]

def _same_suit(suits: list) -> bool:
    return len(set(suits)) == 1

def _suits_and_ranks(community, private) -> tuple:
    community_suits = _strip_suits(community)
    community_rank = _strip_rank(community)
    private_suits = _strip_suits(private) 
    private_rank = _strip_rank(private)

    total_suits = community_suits + private_suits 
    total_ranks = community_rank + private_rank

    return (total_ranks, total_suits)


def royal_flush(community, private) -> int:
    total_rank, total_suits = _suits_and_ranks(community, private)
    seeking_rank = [14, 13, 12, 11, 10]

    same_suit = _same_suit(total_suits)
    ranks = sorted(total_rank, reverse=True)

    # Only want the first 5 highest to lowest
    perfect_ranks = False
    for item in range(5):
        if ranks[item] not in seeking_rank:
            perfect_ranks = False
            break
        perfect_ranks = True

    if same_suit and perfect_ranks:
        return 9
    return -1

def straight_flush(community, private) -> int:
    total_ranks, total_suits = _suits_and_ranks(community, private)

    same_suit = _same_suit(total_suits)
    seq_rank = False

    # TODO
    # same_suit = True
    ranks = sorted(set(total_ranks))
    seq_count = 0 
    for iterate in range(len(ranks)):
        if iterate == 0:
            continue
        elif ranks[iterate] - ranks[iterate -1] == 1:
            seq_count += 1

        if seq_count >= 4:
            seq_rank = True
            break
    
    # TODO
    # print(seq_count)
    # print(ranks)
    if same_suit and seq_rank:
        return 8
    return -1

def four_kind(community, private) -> int:
    total_ranks, _ = _suits_and_ranks(community, private)

    # TODO
    # total_ranks = [7, 7, 7, 7, 1, 3, 4]
    counter = Counter(total_ranks)        
    rank, count = counter.most_common(1)[0] # Get the first item from list
    if count == 4:
        ranks = set(total_ranks)
        ranks.remove(rank)
        return 7 + max(ranks)/100
    return -1

def full_house(community, private) -> int:
    total_ranks, _ = _suits_and_ranks(community, private)

    # TODO
    # total_ranks = [4, 7, 7, 8, 4, 1]
    counter = Counter(total_ranks)
    freq = counter.most_common(2)
    first = freq[0][1]
    second = freq[1][1]
    if first == 3 and second == 2:
        return 6
    return -1

def flush(community, private) -> int:
    _, total_suits = _suits_and_ranks(community, private)

    counter = Counter(total_suits)
    suit = counter.most_common(1)[0][1]
    if suit == 5:
        return 5
    return -1

def straight(community, private) -> int:
    total_ranks, _ = _suits_and_ranks(community, private)

    ranks = sorted(set(total_ranks))
    storage = [] # Store the sequences
    seq_count = 0 
    for iterate in range(len(ranks)):
        if iterate == 0:
            continue
        elif ranks[iterate] - ranks[iterate -1] == 1:
            seq_count += 1
            storage.append(ranks[iterate])

    if seq_count >= 4:
        return 4 + max(storage)/10 
    elif seq_count == 3:
        # Low-wheel
        if 14 in ranks and 2 in storage and 3 in storage:
            return 4 + max(storage)/100
        else:
            return -1
    else:
        return -1

def three_kind(community, private) -> int:
    total_ranks, _ = _suits_and_ranks(community, private)

    # TODO
    # total_ranks = [7, 7, 7, 1, 1, 3, 4]
    counter = Counter(total_ranks)        
    rank, count = counter.most_common(1)[0]
    if count == 3:
        ranks = set(total_ranks)
        ranks.remove(rank)
        kicker_one = max(ranks)
        ranks.remove(kicker_one)
        kicker_two = max(ranks)
        return 3 + (kicker_one + kicker_two)/100
    return -1

def two_pair(community, private) -> int:
    total_ranks, _ = _suits_and_ranks(community, private)

    # TODO
    # total_ranks = [7, 7, 5, 1, 1, 3, 4]
    counter = Counter(total_ranks)        
    freq = counter.most_common(2)
    f_rank, first = freq[0]
    s_rank, second = freq[1]
    if first == 2 and first == second:
        ranks = set(total_ranks)
        ranks.remove(f_rank)
        ranks.remove(s_rank)
        kicker = max(ranks)
        return 2 + kicker/100
    return -1

def one_pair(community, private) -> int:
    total_ranks, _ = _suits_and_ranks(community, private)

    # TODO
    # total_ranks = [7, 7, 5, 1, 6, 3, 4]
    counter = Counter(total_ranks)        
    rank, count = counter.most_common(1)[0]
    if count == 2:
        ranks = set(total_ranks)
        ranks.remove(rank)
        kicker_one = max(ranks)
        ranks.remove(kicker_one)
        kicker_two = max(ranks)
        ranks.remove(kicker_two)
        kicker_three = max(ranks)
        return 1 + (kicker_one + kicker_two + kicker_three)/100
    return -1

def high_card(community, private) -> int:
    total_ranks, _ = _suits_and_ranks(community, private)

    ranks = sorted(total_ranks, reverse=True)
    ranks = ranks[:-2] # I don't want the lowest 2
    score_int = int(''.join(f"{rank}" for rank in ranks))
    score_float = score_int / (10 ** (len(ranks) * 2)) # Moving the zero by 2 per rank
        
    return score_float

