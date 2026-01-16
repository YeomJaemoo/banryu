import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import base64

st.set_page_config(
    page_title="pet_map",
    page_icon="🌻"
)
st.title("All maps for pets:📡")
st.text("사이드바에서 찾고 싶은 영역을 지정 후 검색하세요!")
st.divider()
df = pd.read_csv("반려동물데이터.csv", encoding='cp949')

with st.sidebar.form("반려동물"):
    st.subheader("반려동물을 위한 지도 검색🐦")
    
    petmap_category = st.multiselect(
        "카테고리✔️", df["카테고리"].unique())
    
    # 카테고리에 따라 선택 가능한 업종 목록 필터링
    filtered_foundation = df[df["카테고리"].isin(petmap_category)]["업종"].unique()
    button = st.form_submit_button("선택")
    foundation = st.multiselect("업종🚥", filtered_foundation)
    
    select_region = st.multiselect("구 선택🔎", df["구"].unique())
    button = st.form_submit_button("검색")

if button:
    filtered_df = df.copy()
    
    if petmap_category:    
        filtered_df = filtered_df[filtered_df["카테고리"].isin(petmap_category)]
    
    if foundation:    
        filtered_df = filtered_df[filtered_df["업종"].isin(foundation)]
    
    if select_region:
        filtered_df = filtered_df[filtered_df["구"].isin(select_region)]
    
    if filtered_df.empty:
        st.error("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
        st.write(filtered_df)
        for index, row in filtered_df.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"<strong>{row['상호명']}</strong><br><br>\
                    주소: {row['도로명주소']}<br>홈페이지: {row['홈페이지']}<br>휴무일: {row['휴무일']}\
                        <br>오픈시간: {row['오픈시간']}<br>제한사항: {row['제한사항']}<br>주차여부: {row['주차여부']}<br>입장가능종류: {row['입장가능종류']}",
                icon=folium.Icon(color=row["color"], icon="info-sign", prefix="fa")
            ).add_to(m)
        
        folium_static(m)
st.divider()

with st.expander("나의 펫과 추억쌓기🙈🙉🙊"):
    st.text("지도를 통해 검색한 곳을 가기위한 계획을 작성하고, 이미지를 첨부하여 보고서를 작성해보세요.")
    
    # 세션 스테이트를 사용하여 게시판 데이터를 저장
    if 'board' not in st.session_state:
        st.session_state['board'] = []
        
    if st.button('기존 게시글 삭제'):
        st.session_state['board'] = []
        
    # 게시글 작성 폼
    with st.form("계획서 작성"):
        title = st.text_input("학번과 이름")
        content_1 = st.text_area("계획")
        image_1 = st.file_uploader("계획 지도 업로드", type=["png", "jpg", "jpeg"])
        content_2 = st.text_area("보고서")
        image_2 = st.file_uploader("보고서 첨부 이미지 업로드", type=["png", "jpg", "jpeg"])
        submitted_1 = st.form_submit_button("작성")
        
    
    # 작성 버튼이 클릭되었을 때
    if submitted_1:
        # 계획서 추가   
        new_post_1 = {
            "학번과 이름": title,
            "계획": content_1 if content_1 else None,
            "계획 지도": image_1.read() if image_1 is not None else None,
            "보고서": content_2 if content_2 else None,
            "보고서 첨부 이미지": image_2.read() if image_2 is not None else None,
        }
        st.session_state['board'].append(new_post_1)
    
    # 게시판 출력
    for idx, post in enumerate(reversed(st.session_state['board'])):
        st.write(f"## 계획서 및 보고서 {idx+1}")
        st.write(f"**학번과 이름:** {post['학번과 이름']}")
        if post.get('계획') is not None:
            st.write(f"**계획:** {post['계획']}")
        if post.get('계획 지도') is not None:
            st.image(post['계획 지도'], use_column_width=True)
        if post.get('보고서') is not None:
            st.write(f"**보고서:** {post['보고서']}")
        if post.get('보고서 첨부 이미지') is not None:
            st.image(post['보고서 첨부 이미지'], use_column_width=True)
        
        # 게시글 다운로드 링크 생성
        csv = f"학번과 이름: {post['학번과 이름']}\n"
        if post.get('계획') is not None:
            csv += f"계획: {post['계획']}\n"
        if post.get('보고서') is not None:
            csv += f"보고서: {post['보고서']}"
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="계획_및_보고서_{idx+1}.txt">계획 및 보고서 다운로드</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        if post.get('계획 지도') is not None:
            # 계획 지도 다운로드 링크 생성
            b64_img = base64.b64encode(post['계획 지도']).decode()
            img_href = f'<a href="data:image/png;base64,{b64_img}" download="계획_지도_{idx+1}.png">계획 지도 다운로드</a>'
            st.markdown(img_href, unsafe_allow_html=True)
        
        if post.get('보고서 첨부 이미지') is not None:
            # 보고서 첨부 이미지 다운로드 링크 생성
            b64_img = base64.b64encode(post['보고서 첨부 이미지']).decode()
            img_href = f'<a href="data:image/png;base64,{b64_img}" download="보고서_이미지_{idx+1}.png">보고서 첨부 이미지 다운로드</a>'
            st.markdown(img_href, unsafe_allow_html=True)
        
        st.write("---")
