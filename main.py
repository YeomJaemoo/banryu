import streamlit as st
import os

os.chdir(os.getcwd())
st.set_page_config(
    page_title="반려동물과 추억쌓기❤️", 
    page_icon="🦎"
)

st.title("🐰🐱🐶반려동물 도우미🐊🦎🐍")
st.subheader("반려동물을 기를 때 필요한 모든 것이 있다!")

pet = [
    {
        "name": "강아지",
        "type": "포유류",
        "image": r"images\2.png",
        "info": "강아지에 대한 정보입니다."
    },
    {
        "name": "고양이",
        "type": "포유류",
        "image": r"images\3.png",
        "info": "고양이에 대한 정보입니다."
    },
    {
        "name": "앵무새",
        "type": "조류",
        "image": r"images\4.png",
        "info": "앵무새에 대한 정보입니다."
    },
    {
        "name": "카멜레온",
        "type": "파충류",
        "image": r"images\5.png",
        "info": "카멜레온에 대한 정보입니다."
    },
    {
        "name": "장수풍뎅이",
        "type": "곤충",
        "image": r"images\6.png",
        "info": "장수풍뎅이에 대한 정보입니다."
    },
    {
        "name": "금붕어",
        "type": "어류",
        "image": r"images\7.png",
        "info": "금붕어에 대한 정보입니다."
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
                st.subheader(current_pet["name"])
                st.image(current_pet["image"])
                st.write(current_pet["info"])
