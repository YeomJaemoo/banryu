import streamlit as st
import os

os.chdir(os.getcwd())
st.set_page_config(
    page_title="반려동물과 추억쌓기❤️", 
    page_icon="🦎"
)

st.title("🐰🐱🐶반려동물 도우미🐊🦎🐍")
st.divider()
st.subheader("반려동물을 기를 때 필요한 모든 것이 있다!")

st.divider()

pet = [
    {
        "name": "강아지",
        "type": "포유류",
        "image": r'images/2.png',
        "info": r'images/8.png'
    },
    {
        "name": "고양이",
        "type": "포유류",
        "image": r"images/3.png",
        "info": r'images/9.png'
    },
    {
        "name": "앵무새",
        "type": "조류",
        "image": r"images/4.png",
        "info": r'images/10.png'
    },
    {
        "name": "이구아나",
        "type": "파충류",
        "image": r"images/5.png",
        "info": r'images/11.png'
    },
    {
        "name": "장수풍뎅이",
        "type": "곤충",
        "image": r"images/6.png",
        "info": r'images/12.png'
    },
    {
        "name": "금붕어",
        "type": "어류",
        "image": r"images/7.png",
        "info": r'images/13.png'
    }
]


for i in range(0,len(pet),3):
    row_pet = pet[i:i+3]
    cols = st.columns(3)
    
    for j in range(len(row_pet)):
        with cols[j%3]:
            current_pet = row_pet[j]
            st.subheader(current_pet["name"])
            st.image(current_pet["image"])
            with st.expander(label=current_pet["type"], expanded=False):
                st.image(current_pet["info"])
             
