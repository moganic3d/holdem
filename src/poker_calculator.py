import itertools
from collections import Counter

class PokerCalculator:
    def __init__(self):
        self.ranks = '23456789TJQKA'
        self.suits = 'HDCS'
        self.deck = [r + s for r in self.ranks for s in self.suits]
        
        self.rank_names = {
            'T': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King', 'A': 'Ace'
        }
        self.suit_names = {
            'H': '하트', 'D': '다이아몬드', 
            'C': '클로버', 'S': '스페이드'
        }

    def get_card_name(self, card):
        if card == "없음":
            return "선택 안함"
        rank = self.rank_names.get(card[0], card[0])
        suit = self.suit_names[card[1]]
        return f"{rank} of {suit}"

    def evaluate_hand(self, cards):
        # 카드의 숫자와 무늬 분리
        ranks = [card[0] for card in cards]
        suits = [card[1] for card in cards]
        
        # 페어, 트리플, 포카드 확인
        rank_counts = Counter(ranks)
        
        # 플러시 확인
        is_flush = len(set(suits)) == 1
        
        # 스트레이트 확인
        rank_values = [self.ranks.index(r) for r in ranks]
        rank_values.sort()
        is_straight = (len(set(rank_values)) == 5 and
                      max(rank_values) - min(rank_values) == 4)
        
        # 핸드 랭크 결정
        if is_straight and is_flush:
            return 8, "스트레이트 플러시"
        elif 4 in rank_counts.values():
            return 7, "포카드"
        elif sorted(rank_counts.values()) == [2,3]:
            return 6, "풀하우스"
        elif is_flush:
            return 5, "플러시"
        elif is_straight:
            return 4, "스트레이트"
        elif 3 in rank_counts.values():
            return 3, "트리플"
        elif list(rank_counts.values()).count(2) == 2:
            return 2, "투페어"
        elif 2 in rank_counts.values():
            return 1, "원페어"
        else:
            return 0, "하이카드"

    def calculate_odds(self, hole_cards, community_cards=[]):
        remaining_cards = [card for card in self.deck 
                         if card not in hole_cards + community_cards]
        
        total_hands = 0
        hand_types = Counter()
        
        cards_needed = 5 - len(community_cards)
        for additional_cards in itertools.combinations(remaining_cards, cards_needed):
            total_cards = list(hole_cards) + list(community_cards) + list(additional_cards)
            for final_hand in itertools.combinations(total_cards, 5):
                rank, hand_type = self.evaluate_hand(final_hand)
                hand_types[hand_type] += 1
                total_hands += 1
        
        results = []
        for hand_type, count in sorted(hand_types.items(), 
                                     key=lambda x: (-x[1], x[0])):
            probability = (count / total_hands) * 100
            results.append({
                "hand":
