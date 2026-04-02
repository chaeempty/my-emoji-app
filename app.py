import streamlit as st
import google.generativeai as genai
import io
from PIL import Image
import requests

# 1. 나(Gemini)와 연결하기 위한 키 설정
GOOGLE_API_KEY = "AIzaSyB0uSz8vACtli0nJfWNEygtmy-hJtKJeIc"
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="Gemini x 기획자 이모지소", layout="wide")
st.title("🤖 Gemini 전용 아이콘 제작소")

# 기획자님의 4가지 스타일 로직 (나에게 내리는 특수 명령)
style_prompts = {
    "2D 볼드 라인": "2D bold line illustration icon, thick black outlines, flat solid colors, white background.",
    "3D 장난감": "3D cute plastic toy style, soft lighting, vibrant colors, white background, high quality.",
    "미니멀 플랫": "Minimalist flat vector icon, clean geometric shapes, flat colors, no shadows.",
    "블랙 라인 아트": "Minimalist black line art, thin uniform strokes, vector style, white background."
}

with st.sidebar:
    st.header("🎨 스타일 엔진")
    style_option = st.radio("테마를 선택하세요:", list(style_prompts.keys()))

user_input = st.text_input("무엇을 그릴까요? (영문 추천)", placeholder="예: coffee, rocket, success")

if st.button("Gemini에게 생성 요청하기", use_container_width=True):
    if not user_input:
        st.warning("내용을 입력해 주세요.")
    else:
        with st.spinner("Gemini가 기획안에 맞게 그리는 중..."):
            try:
                # 구글의 이미지 생성 모델 'imagen-3' 호출
                model = genai.ImageGenerationModel("imagen-3")
                full_prompt = f"{user_input}. {style_prompts[style_option]}"
                
                result = model.generate_images(
                    prompt=full_prompt,
                    number_of_images=1,
                )
                
                # 결과 이미지 가져오기
                img = result.images[0].pil_image
                st.image(img, use_container_width=True)
                
                # 다운로드 버튼
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("이미지 저장하기", buf.getvalue(), f"{user_input}.png", "image/png")
                
            except Exception as e:
                st.error(f"연결 오류: {e}")
                st.info("Tip: 구글 계정에 따라 이미지 생성 권한이 순차 적용 중일 수 있습니다.")
