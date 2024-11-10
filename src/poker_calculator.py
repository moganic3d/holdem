import itertools
from collections import Counter

class PokerCalculator:
    def __init__(self):
        self.ranks = '23456789TJQKA'
        self.suits = 'HDCS'
        self.deck = [r + s for r in self.ranks for s in self.suits]
        
        # 카드 이름 매핑
        self.rank_names = {
            'T': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King', 'A': 'Ace'
        }
        self.suit_names = {
            'H': '하트', 'D': '다이아몬드', 
            'C': '클로버', 'S': '스페이드'
        }

    def get_card_name(self, card):
        rank = self.rank_names.get(card[0], card[0])
        suit = self.suit_names[card[1]]
        return f"{rank} of {suit}"

    # evaluate_hand 메서드는 이전 코드와 동일
    # calculate_odds 메서드는 약간 수정하여 결과를 반환하도록 변경

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
                "hand": hand_type,
                "probability": probability
            })
        
        return results 