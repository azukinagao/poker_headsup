# # hand_eval.py

from itertools import combinations

rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
              '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

HAND_RANKS = {
    9: "Royal Flush",
    8: "Straight Flush",
    7: "Four of a Kind",
    6: "Full House",
    5: "Flush",
    4: "Straight",
    3: "Three of a Kind",
    2: "Two Pair",
    1: "One Pair",
    0: "High Card"
}

def rank_value(rank):
    return rank_order[rank]

def is_flush(cards):
    suits = [card.suit for card in cards]
    return len(set(suits)) == 1

def is_straight(ranks):
    ranks = sorted(set(ranks))
    if len(ranks) < 5:
        return False
    for i in range(len(ranks) - 4):
        if ranks[i+4] - ranks[i] == 4:
            return True
    if set([14, 2, 3, 4, 5]).issubset(set(ranks)):
        return True
    return False

def evaluate_5card_hand(cards):
    ranks = [rank_value(card.rank) for card in cards]
    suits = [card.suit for card in cards]
    rank_counts = {r: ranks.count(r) for r in set(ranks)}
    unique_counts = sorted(rank_counts.values(), reverse=True)

    flush = is_flush(cards)
    straight = is_straight(ranks)

    if flush and straight:
        if set([10, 11, 12, 13, 14]).issubset(ranks):
            return (9, max(ranks))  # ロイヤルフラッシュ
        return (8, max(ranks))      # ストレートフラッシュ
    if 4 in unique_counts:
        return (7, max(rank for rank, count in rank_counts.items() if count == 4))  # フォーカード
    if 3 in unique_counts and 2 in unique_counts:
        return (6, max(rank for rank, count in rank_counts.items() if count == 3))  # フルハウス
    if flush:
        return (5, max(ranks))  # フラッシュ
    if straight:
        return (4, max(ranks))  # ストレート
    if 3 in unique_counts:
        return (3, max(rank for rank, count in rank_counts.items() if count == 3))  # スリーカード
    if unique_counts.count(2) == 2:
        return (2, max(rank for rank, count in rank_counts.items() if count == 2))  # ツーペア
    if 2 in unique_counts:
        return (1, max(rank for rank, count in rank_counts.items() if count == 2))  # ワンペア
    return (0, max(ranks))  # ハイカード

def evaluate_hand(cards):
    best = (0, 0)
    for combo in combinations(cards, 5):
        val = evaluate_5card_hand(combo)
        if val > best:
            best = val
    return best, HAND_RANKS[best[0]]
