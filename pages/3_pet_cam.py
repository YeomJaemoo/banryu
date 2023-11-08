import streamlit as st
import cv2
import numpy as np
import base64

st.set_page_config(
    page_title="pet_cam",
    page_icon="🏳️‍🌈"
)

# 이미지 데이터 변환 함수
def convert_image_to_bytes(image):
    _, buffer = cv2.imencode('.png', image)
    bytes_data = buffer.tobytes()
    return bytes_data

# 카메라 입력
img_file_buffer = st.camera_input("📸펫과 함께한 추억을 사진으로 남기세요!")

# 사용자가 업로드한 이미지 가져오기
uploaded_image = st.file_uploader("워터마크 사진 정하기", type=["png", "jpg", "jpeg"])

# 카메라 이미지 변수 초기화
camera_image = None

if img_file_buffer is not None:
    # 카메라 촬영 이미지 읽기
    bytes_data = img_file_buffer.getvalue()
    camera_image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # 사용자가 업로드한 이미지 읽기
    if uploaded_image is not None:
        uploaded_bytes = uploaded_image.getvalue()
        uploaded_cv2_img = cv2.imdecode(np.frombuffer(uploaded_bytes, np.uint8), cv2.IMREAD_COLOR)

        # 이미지 크기 조정
        uploaded_cv2_img = cv2.resize(uploaded_cv2_img, (camera_image.shape[1], camera_image.shape[0]))

        # 이미지 합성
        combined_image = cv2.addWeighted(camera_image, 0.9, uploaded_cv2_img, 0.1, 0)
        st.image(combined_image, channels="BGR")

    else:
        st.image(camera_image, channels="BGR")

with st.expander("**나의 펫**🐾 관찰일지📰"):
    st.subheader("🙂반려 동물의 상태를 기록하고 사진을 찍어 관찰일지를 작성해요.😋")
    # 세션 스테이트를 사용하여 게시판 데이터를 저장
    if 'board' not in st.session_state:
        st.session_state['board'] = []
        
    if st.button('기존 게시글 삭제'):
        st.session_state['board'] = []
        
    # 게시글 작성 폼
    with st.form("게시글 작성"):
        title = st.text_input("학번과 이름")
        content = st.text_area("일지 내용")
        if camera_image is not None:
            image = st.image(camera_image, channels="BGR")
        else:
            image = None
        submitted = st.form_submit_button("작성")
    
    # 게시글 작성 버튼이 클릭되었을 때
    if submitted:
        # 게시글 추가   
        new_post = {"학번과 이름": title, "일지 내용": content if content else None, "이미지": convert_image_to_bytes(camera_image) if camera_image is not None else None}
        st.session_state['board'].append(new_post)
    
    
    # 게시판 출력
    for idx, post in enumerate((st.session_state['board'])):
        st.write(f"## 계획과 보고서 {idx+1}")
        st.write(f"**학번과 이름:** {post['학번과 이름']}")
        if post.get('일지 내용') is not None:
            st.write(f"**일지 내용:** {post['일지 내용']}")
        if post.get('이미지') is not None:
            st.image(post['이미지'], use_column_width=True)
        
        # 게시글 다운로드 링크 생성
        csv = f"학번과 이름: {post['학번과 이름']}\n"
        if post.get('일지 내용') is not None:
            csv += f"일지 내용: {post['일지 내용']}\n"
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="게시글_{idx+1}.txt">게시글 다운로드</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        if post.get('이미지') is not None:
            # 이미지 다운로드 링크 생성
            b64_img = base64.b64encode(post['이미지']).decode()
            img_href = f'<a href="data:image/png;base64,{b64_img}" download="이미지_{idx+1}.png">이미지 다운로드</a>'
            st.markdown(img_href, unsafe_allow_html=True)
        
        st.write("---")
