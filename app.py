import streamlit as st
from poker_calculator import PokerCalculator
import os

st.set_page_config(
    page_title="포커 확률 계산기",
    page_icon="🎲",
    layout="wide"
)

def main():
    st.title("🎲 텍사스 홀덤 확률 계산기")
    
    calc = PokerCalculator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("홀 카드 선택")
        hole_card1 = st.selectbox(
            "첫 번째 카드",
            options=calc.deck,
            format_func=calc.get_card_name,
            key="hole1"
        )
        
        hole_card2 = st.selectbox(
            "두 번째 카드",
            options=[c for c in calc.deck if c != hole_card1],
            format_func=calc.get_card_name,
            key="hole2"
        )
    
    with col2:
        st.subheader("커뮤니티 카드 선택")
        community_cards = []
        
        remaining_cards = [c for c in calc.deck 
                         if c not in [hole_card1, hole_card2]]
        
        for i in range(5):
            card = st.selectbox(
                f"커뮤니티 카드 {i+1}",
                options=["없음"] + [c for c in remaining_cards 
                                if c not in community_cards],
                format_func=lambda x: calc.get_card_name(x) if x != "없음" else "선택 안함",
                key=f"community{i}"
            )
            if card != "없음":
                community_cards.append(card)
    
    if st.button("확률 계산하기"):
        results = calc.calculate_odds([hole_card1, hole_card2], community_cards)
        
        st.subheader("계산 결과")
        for result in results:
            st.metric(
                label=result["hand"],
                value=f"{result['probability']:.2f}%"
            )

if __name__ == "__main__":
    main() 