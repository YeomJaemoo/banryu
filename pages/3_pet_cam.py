import streamlit as st
import cv2
import numpy as np

st.set_page_config(
    page_title="pet_cam",
    page_icon="🏳️‍🌈"
)
# 카메라 입력
img_file_buffer = st.camera_input("Take a picture")

# 사용자가 업로드한 이미지 가져오기
uploaded_image = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg"])

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
        combined_image = cv2.addWeighted(camera_image, 0.5, uploaded_cv2_img, 0.5, 0)
        st.image(combined_image, channels="BGR")

    else:
        st.image(camera_image, channels="BGR")
