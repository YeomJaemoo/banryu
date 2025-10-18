import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(
    page_title="pet_chat",
    page_icon="💻"
)
def create_prompt(
    query,
    system_role=f"""You are a pet care specialist and doctor who knows pets well and kindly suggests more than 3 solutions. If you are asked, please provide a solution in detail and make sure to answer in Korean. The person who developed this is Yeom Jae-moo, a technology teacher at Kangsin Middle School.
    """,
    model="gpt-4o-mini",
    stream=True
):
    user_content = f"""User question: "{str(query)}". """

    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": user_content}
    ]
    return messages

def generate_response(messages):
    with st.spinner("작성 중..."):
        result = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4,
            max_tokens=400)
    return result['choices'][0]['message']['content']

st.image('images/ask_me_chatbot.png')

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if st.button('기존 체팅 삭제'):
    st.session_state['generated'] = []
    st.session_state['past'] = []

with st.form('form', clear_on_submit=True):
    user_input = st.text_input('😎반려동물의 어떤 문제가 있나요?', '', key='input')
    submitted = st.form_submit_button('제출')

if submitted and user_input:
    # 프롬프트 생성 후 프롬프트를 기반으로 챗봇의 답변을 반환
    prompt = create_prompt(user_input)
    chatbot_response = generate_response(prompt)
    st.balloons()
    
    
    st.session_state['past'].append(user_input)
    st.session_state["generated"].append(chatbot_response)
        
if st.session_state['generated']:
    for i in reversed(range(len(st.session_state['generated']))):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
